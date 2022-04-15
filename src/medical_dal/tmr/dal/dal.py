import json
from dataclasses import dataclass
from typing import List

import logbook
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.database import Database

from tmr_common.data_models.patient import Patient

logger = logbook.Logger(__name__)


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
                self.db.patients.find({"admission.department": department, "admission.wing": wing}, {"admission": 1})]

    def get_patient_by_id(self, patient: str) -> dict:
        return self.db.patients.find_one({"_id": ObjectId(patient)})

    def get_patient_by_bed(self, department: str, wing: str, bed: str) -> str:
        res = self.db.patients.find_one({"admission": {"department": department, "wing": wing, "bed": bed}})
        return str(res.pop('_id')) if res else None

    def update_patient_by_id(self, patient: str, update_object: dict) -> bool:
        update_result = self.db.patients.update_one({"_id": ObjectId(patient)}, {'$set': update_object})
        return update_result.modified_count

    def update_patient_by_bed(self, department: str, wing: str, bed: str, update_object: dict):
        update_result = self.db.patients.update_one(
            {"admission": {"department": department, "wing": wing, "bed": bed}},
            {'$set': update_object}
        )
        return update_result.modified_count

    def get_patient_measures(self, patient: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"_id": ObjectId(patient)}, {"measures": 1})))

    def append_warning_to_patient_by_id(self, patient: str, warning: str) -> bool:
        update_result = self.db.patients.update_one(
            {"_id": ObjectId(patient)},
            {'$push': {"warnings": {ObjectId(), warning}}}
        )
        return update_result.modified_count
