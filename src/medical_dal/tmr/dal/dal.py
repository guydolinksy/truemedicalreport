import json
from dataclasses import dataclass
from enum import Enum
from typing import List

import logbook
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.database import Database

from tmr_common.data_models.patient import Patient, Admission, Severity
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
        return [Patient(oid=str(patient.pop("_id")), **patient) for patient in
                self.db.patients.find({"admission.department": department, "admission.wing": wing},
                                      {"_id": 1, "admission": 1, "chameleon_id": 1, 'name': 1})]

    def get_department_patients(self, department: str) -> List[Patient]:
        return [Patient(oid=str(patient.pop("_id")), **patient) for patient in
                self.db.patients.find({"admission.department": department},
                                      {"_id": 1, "admission": 1, "chameleon_id": 1, 'name': 1})]

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
                patient.severity = patient.esi
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

    @staticmethod
    async def notify_admission(admission: Admission):
        if admission:
            await notify('admission', admission.dict())

    @staticmethod
    async def notify_patient(patient: str):
        if patient:
            await notify('patient', patient)
