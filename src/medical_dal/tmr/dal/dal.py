from dataclasses import dataclass
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
from pymongo.database import Database
from pymongo.results import UpdateResult


@dataclass
class MedicalDal:
    db: Database

    def patient_count_in_wing(self, wing_id: str) -> int:
        return self.db.patients.count_documents({"wing_id": ObjectId(wing_id)})

    def patients_in_wing(self, wing_id: str) -> dict:
        return json.loads(dumps(self.db.patients.find({"wing_id": ObjectId(wing_id)}, {"bed": 1})))

    def get_wing_details(self, wing_id: str) -> dict:
        return json.loads(dumps(self.db.wings.find_one({"_id": ObjectId(wing_id)})))

    def get_all_wings_names(self) -> dict:
        return json.loads(dumps(self.db.wings.find({}, {"name": 1})))

    def get_patient_info_by_id(self, patient_id: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"_id": ObjectId(patient_id)})))

    def update_patient_info_by_id(self, patient_id: str, path: list, value: any, data: dict) -> bool:
        self.db.patients.update_one(
            {"_id": ObjectId(patient_id)},
            {'$set': {path[0]: value}}
        )
        return True

    def get_patient_info_by_bed(self, bed: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"bed": bed})))

    def append_warning_to_patient_by_id(self, patient_id: str, warning: str) -> bool:
        update_result: UpdateResult = self.db.patients.update_one(
            {"_id": ObjectId(patient_id)},
            {'$push': {"warnings": {ObjectId(), warning}}}
        )
        return update_result.modified_count >= 1
