from dataclasses import dataclass

from pymongo.collection import Collection


@dataclass
class MedicalDal:
    patients: Collection

    def patient_count_in_wing(self, wing_id: int) -> int:
        return self.patients.count_documents({"wing_id": wing_id})

    def wing_structure(self, wing_id: int) -> dict:
        return self.patients.find({"wing_id": wing_id})
