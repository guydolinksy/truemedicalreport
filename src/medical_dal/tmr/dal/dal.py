import datetime
import json
from dataclasses import dataclass
from enum import Enum
from typing import List

import logbook
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.database import Database
from werkzeug.exceptions import NotFound

from tmr_common.data_models.aggregate.medical_sum import WaitForDoctor, MedicalSum
from tmr_common.data_models.councils import Councils
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.labs import LabTest, LabCategory, LabStatus, StatusInHebrew
from tmr_common.data_models.measures import Measure, MeasureTypes, FullMeasures, Latest
from tmr_common.data_models.measures import Measures
from tmr_common.data_models.notification import Notification
from tmr_common.data_models.patient import Patient, Admission, PatientNotifications, ExternalPatient, InternalPatient, \
    PatientInfo, Event
from ..routes.websocket import notify

logger = logbook.Logger(__name__)


class Action(Enum):
    insert = 0
    remove = 1
    update = 2


@dataclass
class MedicalDal:
    db: Database

    def get_department_wings(self, department: str) -> dict:
        return json.loads(dumps(self.db.wings.find({"department": department}, {"_id": 1, "key": 1, "name": 1})))

    def get_wing(self, department: str, wing: str) -> dict:
        return json.loads(dumps(self.db.wings.find_one({"department": department, "key": wing})))

    def get_wing_patient_count(self, department: str, wing: str) -> int:
        return self.db.patients.count_documents({"admission.department": department, "admission.wing": wing})

    def get_wing_patients(self, department: str, wing: str) -> List[Patient]:
        patients = [Patient(oid=str(patient.pop("_id")), **patient) for patient in
                    self.db.patients.find({"admission.department": department, "admission.wing": wing})]
        return patients

    def get_wing_notifications(self, department: str, wing: str) -> List[PatientNotifications]:
        patients = {patient.external_id: patient for patient in self.get_wing_patients(department, wing)}
        notifications = {external_id: [] for external_id in patients}
        for notification in self.db.notifications.find({"patient_id": {'$in': list(notifications)}}):
            notification = Notification(oid=str(notification.pop("_id")), **notification)
            notifications[notification.patient_id].append(notification)

        return sorted([
            PatientNotifications(
                patient=patients[patient],
                notifications=sorted(notifications, key=lambda n: datetime.datetime.fromisoformat(n.at), reverse=True)
            ) for patient, notifications in notifications.items() if
            notifications or patients[patient].flagged
        ], key=lambda pn: (
            bool(pn.patient.flagged),
            datetime.datetime.fromisoformat(pn.at) if pn.at else datetime.datetime.min
        ), reverse=True)

    def get_department_patients(self, department: str) -> List[Patient]:
        return [Patient(**p) for p in self.db.patients.find({"admission.department": department})]

    def get_patient_images(self, patient: str) -> List[Imaging]:
        return [Imaging(oid=str(image.pop("_id")), **image) for image in self.db.images.find({"patient_id": patient})]

    def get_patient_councils(self, patient: str) -> List[Councils]:
        return [Councils(oid=str(council.pop("_id")), **council) for council in
                self.db.councils.find({"patient_id": patient})]

    def get_patient_labs(self, patient: str) -> List[LabTest]:
        return [LabTest(oid=str(labs.pop("_id")), **labs) for labs in self.db.labs.find({"patient_id": patient})]

    def get_patient_by_id(self, patient: str) -> Patient:
        res = self.db.patients.find_one({"_id": ObjectId(patient)})
        if not res:
            raise NotFound()
        return Patient(**res)

    def get_patient_info_by_id(self, patient: str) -> PatientInfo:
        res = self.db.patients.find_one({"_id": ObjectId(patient)})
        if not res:
            raise NotFound()
        patient = Patient(**res)
        imaging = [Imaging(**res) for res in self.db.imaging.find({"patient_id": patient.external_id})]
        measures = FullMeasures(
            measures=[Measure(**d) for d in self.db.measures.find({"patient_id": patient.external_id})]
        )
        labs = [LabCategory(**tube) for tube in self.db.labs.find({"patient_id": patient.external_id})]
        events = [Event(content='קבלה למחלקה', at=patient.arrival, key='arrival')]
        return PatientInfo(
            imaging=imaging,
            full_measures=measures,
            events=events,
            labs=labs,
            **patient.dict()
        ) if res else None

    def get_patient_by_bed(self, department: str, wing: str, bed: str) -> str:
        res = self.db.patients.find_one({"admission": {"department": department, "wing": wing, "bed": bed}})
        return str(res.pop('_id')) if res else None

    async def update_patient_by_id(self, patient: str, update_object: dict) -> bool:
        update_result = self.db.patients.update_one({"_id": ObjectId(patient)}, {'$set': update_object})

        await self.notify_patient(patient)
        return update_result.modified_count

    async def upsert_patient(self, previous: Patient, patient: ExternalPatient):
        if previous and patient:
            self.db.patients.update_one({"external_id": patient.external_id},
                                        {'$set': patient.dict()})
        elif previous and not patient:
            self.db.patients.delete_one({"external_id": previous.external_id})
        elif not previous and patient:
            self.db.patients.update_one({"external_id": patient.external_id}, {'$set': dict(
                **patient.dict(),
                **InternalPatient.from_external_patient(patient).dict()
            )}, upsert=True)

        if previous and (not patient or previous.admission != patient.admission):
            await self.notify_admission(admission=previous.admission)
        if patient:
            new_patient = self.db.patients.find_one({"external_id": patient.external_id})
            if not new_patient:
                raise ValueError('Patient not inserted')
            new_patient = Patient(**new_patient)
            if not previous or previous.admission != new_patient.admission:
                await self.notify_admission(admission=new_patient.admission)
            if not previous or previous.dict() != new_patient.dict():
                await self.notify_patient(patient=new_patient.oid)

    def get_patient_measures(self, patient: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"_id": ObjectId(patient)}, {"measures": 1})))

    def append_warning_to_patient_by_id(self, patient: str, warning: str) -> bool:
        update_result = self.db.patients.update_one(
            {"_id": ObjectId(patient)},
            {'$push': {"warnings": {ObjectId(), warning}}}
        )
        return update_result.modified_count

    async def upsert_measurements(self, patient_id: str, measures: List[Measure]):
        res = self.db.patients.find_one({"external_id": patient_id})
        if not res:
            logger.error(f'Measurement Patient {patient_id} Not Fount')
            return
        previous = Patient(**res)
        current = previous.measures.copy()

        for measure in measures:
            match measure.type:
                case MeasureTypes.pulse.value:
                    if not current.pulse or measure.at_ > current.pulse.at_:
                        current.pulse = Latest(value=int(measure.value), at=measure.at, is_valid=measure.is_valid)
                case MeasureTypes.temperature.value:
                    if not current.temperature or measure.at_ > current.temperature.at_:
                        current.temperature = Latest(value=measure.value, at=measure.at, is_valid=measure.is_valid)
                case MeasureTypes.saturation.value:
                    if not current.saturation or measure.at_ > current.saturation.at_:
                        current.saturation = Latest(value=int(measure.value), at=measure.at, is_valid=measure.is_valid)
                case MeasureTypes.systolic.value:
                    if not current.systolic or measure.at_ > current.systolic.at_:
                        current.systolic = Latest(value=int(measure.value), at=measure.at, is_valid=measure.is_valid)
                case MeasureTypes.diastolic.value:
                    if not current.diastolic or measure.at_ > current.diastolic.at_:
                        current.diastolic = Latest(value=int(measure.value), at=measure.at, is_valid=measure.is_valid)
            self.db.measures.update_one({"external_id": measure.external_id},
                                        {'$set': dict(patient_id=patient_id, **measure.dict())}, upsert=True)
        self.db.patients.update_one({"external_id": patient_id},
                                    {'$set': {"measures": Measures(**current.dict()).dict()}}, upsert=True)
        if previous.measures != current:
            await self.notify_patient(patient=previous.oid)

    async def upsert_imaging(self, imaging_obj: Imaging, action: Action):
        res = self.db.patients.find_one({"external_id": imaging_obj.patient_id})
        if not res:
            logger.error(f'Imaging Patient {imaging_obj.patient_id} Not Fount')
            return
        patient = Patient(**res)
        match action:
            case Action.remove:
                pass
            case Action.insert:
                self.db.imaging.update_one({"external_id": imaging_obj.external_id},
                                           {'$set': imaging_obj.dict()}, upsert=True)
                notification = imaging_obj.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await self.notify_patient(patient=patient.oid)
                await self.notify_notification(patient=patient.oid)
            case Action.update:
                self.db.imaging.update_one({"external_id": imaging_obj.external_id},
                                           {'$set': imaging_obj.dict()}, upsert=True)
                notification = imaging_obj.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await self.notify_patient(patient=patient.oid)
                await self.notify_notification(patient=patient.oid)

    async def upsert_labs(self, patient_id: str, new_labs: List[LabTest]):
        labs = {c.key: c for c in [LabCategory(**c) for c in self.db.labs.find({"patient_id": patient_id})]}
        for lab in new_labs:
            c = labs.setdefault(lab.category_key, LabCategory(
                at=lab.at, category_id=lab.category_id, category=lab.category_name
            ))
            c.results[str(lab.test_type_id)] = lab
            c.status = StatusInHebrew[min({l.status for l in c.results.values()})]
        for category in labs.values():
            logger.debug(category.dict())
            self.db.labs.update_one({"patient_id": patient_id, **category.query_key},
                                    {'$set': dict(patient_id=patient_id, **category.dict())}, upsert=True)

    async def upsert_councils(self, councils_obj: Councils, action: Action):
        res = self.db.patients.find_one({"external_id": str(councils_obj.patient_id)})
        if not res:
            logger.error(f'Councils, Patient {councils_obj.patient_id} Not Fount')
            return
        patient = Patient(**res)
        match action:
            case Action.remove:
                pass
            case Action.insert:
                self.db.councils.update_one({"external_id": councils_obj.external_id},
                                            {'$set': councils_obj.dict()}, upsert=True)
                await self.notify_patient(patient=patient.oid)
                await self.notify_notification(patient=patient.oid)
            case Action.update:
                self.db.councils.update_one({"external_id": councils_obj.external_id},
                                            {'$set': councils_obj.dict()}, upsert=True)
                await self.notify_patient(patient=patient.oid)
                await self.notify_notification(patient=patient.oid)

    def get_waiting_for_doctor_list(self) -> [WaitForDoctor]:
        patient_waiting_for_doctor = self.db.councils. \
            aggregate([{"$match": {"arrived": None}}, {
            "$group": {
                "_id": "$doctor_name",
                "sum": {"$sum": 1}
            }
        }])
        waiting_for_doctor_list = [WaitForDoctor(oid=str(data.pop("_id")), **data) for data in
                                   patient_waiting_for_doctor]
        return waiting_for_doctor_list

    def get_people_amount_wait_council(self) -> int:
        patient_waiting_for_council = self.db.councils. \
            aggregate([{"$match": {"arrived": None}}, {"$count": "waiting"}])
        return list(patient_waiting_for_council)[0]["waiting"]

    @staticmethod
    async def notify_admission(admission: Admission):
        if admission:
            await notify('admission', admission.dict())

    @staticmethod
    async def notify_notification(patient: str):
        if patient:
            await notify('notification', patient)

    @staticmethod
    async def notify_patient(patient: str):
        if patient:
            await notify('patient', patient)
