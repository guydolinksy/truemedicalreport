from datetime import datetime
from typing import Optional, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from .measures import Measures
from .severity import Severity


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]

    class Config:
        orm_mode = True


class Patient(BaseModel):
    oid: Optional[str]

    # Chameleon fields
    esi: Optional[int]
    name: Optional[str]
    age: Optional[str]
    birthdate: Optional[str]
    complaint: Optional[str]
    admission: Optional[Admission]
    measures: Optional[Measures]

    # Internal fields
    awaiting: Optional[str]
    severity: Optional[Severity]
    flagged: Optional[bool]
    warnings: Optional[List[dict]]

    id_: Optional[str]

    class Config:
        orm_mode = True

    def chameleon_dict(self):
        return {
            "id_": self.id_,
            "name": self.name,
            "age": self.age,
            "birthdate": self.birthdate,
            "complaint": self.complaint,
            "admission": self.admission.dict(),
            "esi": self.esi,
        }
