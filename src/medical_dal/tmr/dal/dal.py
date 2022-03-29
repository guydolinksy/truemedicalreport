from dataclasses import dataclass
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
from pymongo.database import Database


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

    def get_patient_info_by_bed(self, bed: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"bed": bed})))

    def get_patient_measures(self, patient_id: str) -> dict:
        return json.loads(dumps(self.db.patients.find_one({"_id": ObjectId(patient_id)}, {"measures": 1})))
