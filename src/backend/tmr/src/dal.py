from dataclasses import dataclass
from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo.database import Database


@dataclass
class MedicalDal:
    db: Database

    def patient_count_in_wing(self, wing_id: str) -> int:
        return self.db.patients.count_documents({"wing_id": ObjectId(wing_id)})

    def patients_in_wing(self, wing_id: str) -> dict:
        return self.db.patients.find({"wing_id": ObjectId(wing_id)}, {"bed_num": 1})

    def get_wing_details(self, wing_id: str) -> dict:
        return self.db.wings.find_one({"_id": ObjectId(wing_id)})

    def get_patient_info_by_id(self, patient_id: str) -> dict:
        return dumps(self.db.patients.find_one({"_id": ObjectId(patient_id)}))