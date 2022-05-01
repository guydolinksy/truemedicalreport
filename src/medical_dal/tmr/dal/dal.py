import datetime
import json
from dataclasses import dataclass
from enum import Enum
from typing import List

import logbook
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.database import Database

from tmr_common.data_models.measures import Measures
from tmr_common.data_models.patient import Patient, Admission, PatientNotifications
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.notification import Notification
from tmr_common.data_models.severity import Severity
from ..routes.websocket import notify
from tmr_common.data_models.measures import Measures

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
                    self.db.patients.find({"admission.department": department,
                                           "admission.wing": wing},
                                          {"_id": 1,
                                           "admission": 1,
                                           "chameleon_id": 1,
                                           'name': 1,
                                           "notifications": 1})]
        return patients

    def get_wing_notifications(self, department: str, wing: str) -> List[PatientNotifications]:
        patients = {patient.chameleon_id: patient for patient in self.get_wing_patients(department, wing)}
        notifications = {chameleon_id: [] for chameleon_id in patients}
        for notification in self.db.notifications.find({"patient_id": {'$in': list(notifications)}}):
            notification = Notification(oid=str(notification.pop("_id")), **notification)
            notifications[notification.patient_id].append(notification)

        return [PatientNotifications(
            patient=patients[patient],
            notifications=sorted(notifications, key=lambda n: datetime.datetime.fromisoformat(n.at), reverse=True)
        ) for patient, notifications in notifications.items() if notifications]

    def get_department_patients(self, department: str) -> List[Patient]:
        return [Patient(oid=str(patient.pop("_id")), **patient) for patient in
                self.db.patients.find({"admission.department": department},
                                      {"_id": 1, "admission": 1, "chameleon_id": 1, 'name': 1})]

    def get_patient_images(self, patient: str) -> List[Imaging]:
        return [Imaging(oid=str(image.pop("_id")), **image) for image in self.db.images.find({"patient_id": patient})]

    def get_patient_by_id(self, patient: str) -> Patient:
        res = self.db.patients.find_one({"_id": ObjectId(patient)})
        return Patient(oid=str(res.pop("_id")), **res) if res else None

    def get_patient_by_bed(self, department: str, wing: str, bed: str) -> str:
        res = self.db.patients.find_one({"admission": {"department": department, "wing": wing, "bed": bed}})
        return str(res.pop('_id')) if res else None

    async def update_patient_by_id(self, patient: str, update_object: dict) -> bool:
        update_result = self.db.patients.update_one({"_id": ObjectId(patient)}, {'$set': update_object})

        await self.notify_patient(patient)
        return update_result.modified_count

    async def upsert_patient(self, patient: Patient, action: Action):
        match action:
            case Action.remove:
                previous = Patient(**(self.db.patients.find_one({"chameleon_id": patient.chameleon_id}) or {}))
                self.db.patients.delete_one({"chameleon_id": patient.chameleon_id})
                await self.notify_admission(admission=previous.admission)
            case Action.update:
                previous = Patient(**(self.db.patients.find_one({"chameleon_id": patient.chameleon_id}) or {}))
                self.db.patients.update_one({"chameleon_id": patient.chameleon_id},
                                            {'$set': patient.chameleon_dict()}, upsert=True)

                current = Patient(**(self.db.patients.find_one({"chameleon_id": patient.chameleon_id}) or {}))
                if previous.admission != current.admission:
                    await self.notify_admission(admission=previous.admission)
                    await self.notify_admission(admission=current.admission)
                if previous.chameleon_dict() != current.chameleon_dict():
                    await self.notify_patient(patient=current.oid)

            case Action.insert:
                patient.severity = Severity(**patient.esi.dict())
                patient.awaiting = 'מחכה לך'
                self.db.patients.update_one({"chameleon_id": patient.chameleon_id}, {'$set': {
                    **patient.chameleon_dict(),
                    **patient.internal_dict()}
                }, upsert=True)

                current = Patient(**(self.db.patients.find_one({"chameleon_id": patient.chameleon_id}) or {}))
                await self.notify_admission(admission=current.admission)
                await self.notify_patient(patient=current.oid)

    def get_patient_measures(self, patient: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"_id": ObjectId(patient)}, {"measures": 1})))

    def append_warning_to_patient_by_id(self, patient: str, warning: str) -> bool:
        update_result = self.db.patients.update_one(
            {"_id": ObjectId(patient)},
            {'$push': {"warnings": {ObjectId(), warning}}}
        )
        return update_result.modified_count

    async def upsert_measurements(self, chameleon_id: str, measures_obj: Measures):
        previous = Patient(**(self.db.patients.find_one({"chameleon_id": chameleon_id}) or {}))

        self.db.patients.update_one({"chameleon_id": chameleon_id},
                                    {'$set': {"measures": measures_obj.dict()}}, upsert=True)
        current = Patient(**(self.db.patients.find_one({"chameleon_id": chameleon_id}) or {}))
        if previous.measures != current.measures:
            await self.notify_patient(patient=current.oid)

    async def upsert_imaging(self, imaging_obj: Imaging, action: Action):
        patient = Patient(**(self.db.patients.find_one({"chameleon_id": imaging_obj.patient_id}) or {}))
        match action:
            case Action.remove:
                pass
            case Action.insert:
                self.db.imaging.update_one({"chameleon_id": imaging_obj.chameleon_id},
                                           {'$set': imaging_obj.dict()}, upsert=True)
                notification = imaging_obj.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await self.notify_patient(patient=patient.oid)
                await self.notify_notification(patient=patient.oid)
            case Action.update:
                self.db.imaging.update_one({"chameleon_id": imaging_obj.chameleon_id},
                                           {'$set': imaging_obj.dict()}, upsert=True)
                notification = imaging_obj.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await self.notify_patient(patient=patient.oid)
                await self.notify_notification(patient=patient.oid)

    async def upsert_notification(self, patient_id: str, notification: Notification, action: Action):
        patient = Patient(**(self.db.patients.find_one({"chameleon_id": patient_id}) or {}))
        match action:
            case Action.remove:
                self.db.notifications.delete_one({"notification_id": notification.notification_id})

            case Action.insert:
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {"$set": notification.dict()}, upsert=True)
            case Action.update:
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {"$set": notification.dict()}, upsert=True)
        await self.notify_notification(patient=patient.oid)

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
