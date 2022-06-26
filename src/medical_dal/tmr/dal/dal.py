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

from tmr_common.data_models.aggregate.medical_sum import WaitForDoctor
from tmr_common.data_models.referrals import Referral
from tmr_common.data_models.image import Image, ImagingStatus
from tmr_common.data_models.labs import Laboratory, LabCategory, StatusInHebrew, LabStatus
from tmr_common.data_models.measures import Measure, MeasureTypes, FullMeasures, Latest
from tmr_common.data_models.treatment_decision import TreatmentDecision
from tmr_common.data_models.measures import Measures
from tmr_common.data_models.notification import Notification
from tmr_common.data_models.patient import Patient, Admission, PatientNotifications, ExternalPatient, InternalPatient, \
    PatientInfo, Event, Awaiting, AwaitingTypes
from tmr_common.data_models.warnings import PatientWarning
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
        patients = [Patient(**patient) for patient in
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

    def get_patient_images(self, patient: str) -> List[Image]:
        return [Image(oid=str(image.pop("_id")), **image) for image in self.db.images.find({"patient_id": patient})]

    def get_patient_referrals(self, patient: str) -> List[Referral]:
        return [Referral(oid=str(referral.pop("_id")), **referral) for referral in
                self.db.referrals.find({"patient_id": patient})]

    def get_patient_labs(self, patient: str) -> List[Laboratory]:
        return [Laboratory(oid=str(labs.pop("_id")), **labs) for labs in self.db.labs.find({"patient_id": patient})]

    def get_patient_by_id(self, patient: str) -> Patient:
        res = self.db.patients.find_one({"_id": ObjectId(patient)})
        if not res:
            raise NotFound()
        return Patient(**res)

    def get_patient_by_external_id(self, external_id: str) -> Patient:
        res = self.db.patients.find_one({"external_id": external_id})
        if not res:
            raise NotFound()
        return Patient(**res)

    def get_patient_info_by_id(self, patient: str) -> PatientInfo:
        res = self.db.patients.find_one({"_id": ObjectId(patient)})
        if not res:
            raise NotFound()
        patient = Patient(**res)
        imaging = [Image(**res) for res in self.db.imaging.find({"patient_id": patient.external_id})]
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

    async def _cascade_delete_patient(self, patient_external_id):
        """
        delete patient and his data from all collections.
        :param patient_external_id: external_id of patient
        """
        logger.debug(f"Cascade Delete for Patient {patient_external_id}")
        self.db.labs.delete_many({"patient_id": patient_external_id})
        self.db.imaging.delete_many({"patient_id": patient_external_id})
        self.db.measures.delete_many({"patient_id": patient_external_id})
        self.db.referrals.delete_many({"patient_id": patient_external_id})
        self.db.notifications.delete_many({"patient_id": patient_external_id})
        self.db.patients.delete_many({"id_": patient_external_id})

    async def upsert_patient(self, previous: Patient, patient: ExternalPatient):
        if previous and patient:
            self.db.patients.update_one({"external_id": patient.external_id},
                                        {'$set': patient.dict()})
        elif previous and not patient:
            self.db.patients.delete_one({"external_id": patient.external_id})
            await self._cascade_delete_patient(previous.external_id)
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
            logger.error(f'Measurement Patient {patient_id} Not Found')
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

    async def upsert_imaging(self, imaging_obj: Image, action: Action):
        res = self.db.patients.find_one({"external_id": imaging_obj.patient_id})
        if not res:
            logger.error(f'Imaging Patient {imaging_obj.patient_id} Not Found')
            return
        patient = Patient(**res)
        match action:
            case Action.remove:
                pass
            case (Action.insert | Action.update):
                self.db.imaging.update_one({"external_id": imaging_obj.external_id},
                                           {'$set': imaging_obj.dict()}, upsert=True)
                if imaging_obj.status != ImagingStatus.ordered.value:
                    notification = imaging_obj.to_notification()
                    self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                     {'$set': notification.dict()}, upsert=True)
                    await self.notify_notification(patient=patient.oid)
        await self.update_awaiting(patient, AwaitingTypes.imaging, str(imaging_obj.external_id), Awaiting(
            awaiting=imaging_obj.title,
            completed=imaging_obj.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value],
            since=imaging_obj.at,
            limit=3600,
        ))

    async def upsert_labs(self, patient_id: str, new_labs: List[Laboratory]):
        res = self.db.patients.find_one({"external_id": patient_id})
        if not res:
            logger.error(f'Laboratory Patient {patient_id} Not Found')
            return
        patient = Patient(**res)
        labs = {c.key: c for c in [LabCategory(**c) for c in self.db.labs.find({"patient_id": patient_id})]}
        for lab in new_labs:
            c = labs.setdefault(lab.category_key, LabCategory(
                at=lab.at, category_id=lab.category_id, category=lab.category_name
            ))
            c.results[str(lab.test_type_id)] = lab
            c.status = StatusInHebrew[min({l.status for l in c.results.values()})]
        for single_lab in labs.values():
            is_analyzed = single_lab.status == StatusInHebrew[LabStatus.analyzed.value]
            await self.update_awaiting(patient, AwaitingTypes.laboratory, single_lab.get_instance_id(), Awaiting(
                awaiting=single_lab.category,
                completed=is_analyzed,
                since=single_lab.at,
                limit=3600,
            ))
            await self.update_warning(patient, single_lab.get_if_panic())
            self.db.labs.update_one({"patient_id": patient_id, **c.query_key},
                                    {'$set': dict(patient_id=patient_id, **c.dict())}, upsert=True)
            if is_analyzed:
                notification = single_lab.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await self.notify_notification(patient=patient.oid)

    async def upsert_referrals(self, referral_obj: Referral, action: Action):
        res = self.db.patients.find_one({"external_id": str(referral_obj.patient_id)})
        if not res:
            logger.error(f'Referrals Patient {referral_obj.patient_id} Not Found')
            return
        patient = Patient(**res)
        match action:
            case Action.remove:
                pass
            case (Action.insert | Action.update):
                self.db.referrals.update_one({"external_id": referral_obj.external_id},
                                             {'$set': referral_obj.dict()}, upsert=True)
                if referral_obj.completed:
                    notification = referral_obj.to_notification()
                    self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                     {'$set': notification.dict()}, upsert=True)
                    await self.notify_notification(patient=patient.oid)

        await self.update_awaiting(patient, AwaitingTypes.referral, referral_obj.to, Awaiting(
            awaiting=referral_obj.to,
            since=referral_obj.at,
            completed=referral_obj.completed,
            limit=3600,
        ))

    def upsert_treatment_decision(self, patient: int, decision: TreatmentDecision):
        self.db.patients.update_one({"external_id": patient}, {"$set": decision.dict()}, upsert=True)

    def update_from_free_text(self):
        pass

    def get_waiting_for_doctor_list(self) -> [WaitForDoctor]:
        waiting = self.db.referrals. \
            aggregate([{"$match": {"_id": False}}, {
            "$group": {
                "_id": "$to",
                "sum": {"$sum": 1}
            }
        }])
        return [WaitForDoctor(to=data['_id'], count=data['sum']) for data in waiting]

    def get_people_amount_wait_referral(self) -> int:
        res = self.db.Referrals.aggregate([{"$match": {"completed": False}}, {"$count": "waiting"}])
        return list(res)[0]["waiting"]

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

    async def update_awaiting(self, patient: Patient, type_: AwaitingTypes, tag: str, awaiting: Awaiting):
        updated = patient.copy()
        updated.awaiting.setdefault(type_.value, {}).__setitem__(tag, awaiting)
        await self.update_patient_by_id(patient.oid, updated.dict(include={'awaiting'}))

    async def update_warning(self, patient: Patient, warnings: [PatientWarning]) -> None:
        updated = patient.copy()
        updated.warnings += warnings
        await self.update_patient_by_id(patient.oid, updated.dict(include={'warnings'}))
