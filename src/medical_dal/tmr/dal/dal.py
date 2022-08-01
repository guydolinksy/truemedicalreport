import datetime
import json
import traceback
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

import logbook
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import NotFound

from tmr_common.data_models.aggregate.medical_sum import WaitForDoctor
from tmr_common.data_models.image import Image, ImagingStatus
from tmr_common.data_models.labs import Laboratory, LabCategory, StatusInHebrew, LabStatus
from tmr_common.data_models.measures import Measure, MeasureTypes, FullMeasures, Latest
from tmr_common.data_models.notification import Notification
from tmr_common.data_models.patient import Patient, Admission, PatientNotifications, ExternalPatient, InternalPatient, \
    PatientInfo, Event, Awaiting, AwaitingTypes, BasicMedical
from tmr_common.data_models.referrals import Referral
from tmr_common.data_models.treatment import Treatment
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

    def get_patient(self, patient: dict) -> Patient:
        res = self.db.patients.find_one(patient)
        if not res:
            raise NotFound()
        return Patient(**res)

    def get_patient_info(self, patient: dict) -> PatientInfo:
        patient = self.get_patient(patient)
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
        )

    def get_patient_by_bed(self, department: str, wing: str, bed: str) -> str:
        res = self.db.patients.find_one({"admission": {"department": department, "wing": wing, "bed": bed}})
        return str(res.pop('_id')) if res else None

    async def update_patient(self, patient: dict, update: dict, old: dict = None) -> bool:
        if old is None:
            old = self.get_patient(patient).dict(include=set(update), exclude_none=True)
        while any(old.get(k) != update.get(k) for k in update):
            try:
                update_result = self.db.patients.update_one({**patient, **old}, {'$set': update}, upsert=True)
                if update_result.modified_count:
                    break
            except DuplicateKeyError:
                pass
            old = self.get_patient(patient).dict(include=set(update), exclude_none=True)
        else:
            return False
        if update.get('admission') and old.get('admission') != update.get('admission'):
            await self.notify_admission(update.get('admission'))

        return await self.notify_patient(str(self.db.patients.find_one(patient).pop('_id')))

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
        if previous and not patient:
            self.db.patients.delete_one({"external_id": previous.external_id})
            await self._cascade_delete_patient(previous.external_id)
        elif previous and patient:
            await self.update_patient(
                {"_id": ObjectId(previous.oid)},
                patient.dict(exclude_none=True),
                old=previous.dict()
            )
        elif not previous and patient:
            await self.update_patient(
                {"external_id": patient.external_id},
                dict(
                    **patient.dict(exclude_none=True),
                    **InternalPatient.from_external_patient(patient).dict(exclude_none=True)
                ),
                old={}
            )

    async def upsert_measurements(self, patient_id: str, measures: List[Measure]):
        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        for measure in measures:
            match measure.type:
                case MeasureTypes.pulse.value:
                    if not updated.measures.pulse or measure.at_ > updated.measures.pulse.at_:
                        updated.measures.pulse = Latest(value=int(measure.value), at=measure.at,
                                                        is_valid=measure.is_valid)
                case MeasureTypes.temperature.value:
                    if not updated.measures.temperature or measure.at_ > updated.measures.temperature.at_:
                        updated.measures.temperature = Latest(value=measure.value, at=measure.at,
                                                              is_valid=measure.is_valid)
                case MeasureTypes.saturation.value:
                    if not updated.measures.saturation or measure.at_ > updated.measures.saturation.at_:
                        updated.measures.saturation = Latest(value=int(measure.value), at=measure.at,
                                                             is_valid=measure.is_valid)
                case MeasureTypes.systolic.value:
                    if not updated.measures.systolic or measure.at_ > updated.measures.systolic.at_:
                        updated.measures.systolic = Latest(value=int(measure.value), at=measure.at,
                                                           is_valid=measure.is_valid)
                case MeasureTypes.diastolic.value:
                    if not updated.measures.diastolic or measure.at_ > updated.measures.diastolic.at_:
                        updated.measures.diastolic = Latest(value=int(measure.value), at=measure.at,
                                                            is_valid=measure.is_valid)
            self.db.measures.update_one({"external_id": measure.external_id},
                                        {'$set': dict(patient_id=patient_id, **measure.dict())}, upsert=True)

        await self.update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'measures'}, exclude_none=True),
            old=patient.dict()
        )

    async def upsert_imaging(self, imaging_obj: Image):
        patient = self.get_patient({"external_id": imaging_obj.patient_id})

        updated = patient.copy()
        self.db.imaging.update_one({"external_id": imaging_obj.external_id},
                                   {'$set': imaging_obj.dict()}, upsert=True)
        if imaging_obj.status != ImagingStatus.ordered.value:
            notification = imaging_obj.to_notification()
            self.db.notifications.update_one({"notification_id": notification.notification_id},
                                             {'$set': notification.dict()}, upsert=True)
            await self.notify_notification(patient=patient.oid)
        updated.awaiting.setdefault(AwaitingTypes.imaging.value, {}).setdefault(imaging_obj.external_id, Awaiting(
            awaiting=imaging_obj.title,
            since=imaging_obj.at,
            completed=imaging_obj.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value],
            limit=3600,
        ))

        await self.update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'awaiting'}, exclude_none=True),
            old=patient.dict()
        )

    async def upsert_labs(self, patient_id: str, new_labs: List[Laboratory]):
        labs: Dict[tuple, LabCategory] = {
            c.key: c for c in [LabCategory(**c) for c in self.db.labs.find({"patient_id": patient_id})]
        }
        for lab in new_labs:
            c = labs.setdefault(lab.category_key, LabCategory(
                patient_id=patient_id, at=lab.at, category_id=lab.category_id, category=lab.category_name
            ))
            c.results[str(lab.test_type_id)] = lab
            c.status = StatusInHebrew[min({l.status for l in c.results.values()})]

        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        for lab in labs.values():
            self.db.labs.update_one({"patient_id": patient_id, **c.query_key},
                                    {'$set': dict(patient_id=patient_id, **c.dict(exclude={'patient_id'}))},
                                    upsert=True)
            if lab.status == StatusInHebrew[LabStatus.analyzed.value]:
                notification = lab.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await self.notify_notification(patient=patient.oid)
            for key, warning in lab.warnings:
                updated.warnings.setdefault(key, warning)
            updated.awaiting.setdefault(AwaitingTypes.laboratory.value, {}).setdefault(lab.get_instance_id(), Awaiting(
                awaiting=lab.category,
                since=lab.at,
                completed=lab.status == StatusInHebrew[LabStatus.analyzed.value],
                limit=3600,
            ))

        await self.update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'awaiting', 'warnings'}, exclude_none=True),
            old=patient.dict()
        )

    async def upsert_referral(self, referral_obj: Referral):
        patient = self.get_patient({"external_id": referral_obj.patient_id})

        updated = patient.copy()
        self.db.referrals.update_one({"external_id": referral_obj.external_id},
                                     {'$set': referral_obj.dict()}, upsert=True)
        if referral_obj.completed:
            notification = referral_obj.to_notification()
            self.db.notifications.update_one({"notification_id": notification.notification_id},
                                             {'$set': notification.dict()}, upsert=True)
            await self.notify_notification(patient=patient.oid)
        updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).setdefault(referral_obj.to, Awaiting(
            awaiting=referral_obj.to,
            since=referral_obj.at,
            completed=referral_obj.completed,
            limit=3600,
        ))

        await self.update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'awaiting'}, exclude_none=True),
            patient.dict()
        )

    async def upsert_treatment(self, patient_id: str, treatment: Treatment):
        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        updated.treatment = treatment

        await self.update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'treatment'}, exclude_none=True),
            old=patient.dict()
        )

    async def upsert_basic_medical(self, patient_id: str, basic_medical: BasicMedical):
        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        updated.basic_medical = basic_medical
        if basic_medical.doctor_seen_time:
            updated.awaiting[AwaitingTypes.doctor.value]['exam'].completed = True
        if basic_medical.nurse_description:
            updated.awaiting[AwaitingTypes.nurse.value]['exam'].completed = True

        await self.update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'basic_medical', 'awaiting'}, exclude_none=True),
            old=patient.dict()
        )

    def get_waiting_for_doctor_list(self) -> [WaitForDoctor]:
        waiting = self.db.referrals. \
            aggregate([{"$match": {"_id": False}}, {
            "$group": {
                "_id": "$to",
                "sum": {"$sum": 1}
            }
        }])
        return [WaitForDoctor(to=data['_id'], count=data['sum']) for data in waiting]

    def get_people_amount_waiting_doctor(self, department, wing) -> int:
        res = self.db.patients.aggregate(
            [{"$match": {"awaiting.doctor.exam.completed": False, 'admission.department': department,
                         'admission.wing': wing}},
             {"$count": "count"}])
        response_list = list(res)
        if response_list:
            return response_list[0]["count"]
        else:
            return 0

    def get_people_amount_waiting_nurse(self, department, wing) -> int:
        res = self.db.patients.aggregate(
            [{"$match": {"awaiting.nurse.exam.completed": False, 'admission.department': department,
                         'admission.wing': wing}},
             {"$count": "count"}])
        response_list = list(res)
        if response_list:
            return response_list[0]["count"]
        else:
            return 0

    def get_people_amount_waiting_labs(self, department, wing) -> int:
        count = 0
        for labs in self.db.patients.find({'admission.department': department, 'admission.wing': wing},
                                          {"awaiting.laboratory": 1, "_id": 0}):
            if "False" in str(labs):
                count = count + 1
        return count

    def get_people_amount_waiting_imaging(self, department, wing) -> int:
        count = 0
        for image in self.db.patients.find({'admission.department': department, 'admission.wing': wing},
                                           {"awaiting.imaging": 1, "_id": 0}):
            if "False" in str(image):
                count = count + 1
        return count

    def get_people_amount_waiting_referrals(self, department, wing) -> int:
        count = 0
        for referral in self.db.patients.find({'admission.department': department, 'admission.wing': wing},
                                              {"awaiting.referral": 1, "_id": 0}):
            if "False" in str(referral):
                count = count + 1
        return count

    @staticmethod
    async def notify_admission(admission: dict):
        if admission:
            await notify('admission', admission)

    @staticmethod
    async def notify_notification(patient: str):
        if patient:
            await notify('notification', patient)

    @staticmethod
    async def notify_patient(patient: str) -> bool:
        if not patient:
            return False

        return await notify('patient', patient)
