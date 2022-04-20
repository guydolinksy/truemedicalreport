from datetime import datetime
from typing import Optional, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from .measures import Measures
from .severity import Severity
from .esi_score import ESIScore


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]

    class Config:
        orm_mode = True


class Patient(BaseModel):
    oid: Optional[str]

    # Chameleon fields
    chameleon_id: Optional[str]
    id_: Optional[str]
    esi: Optional[ESIScore]
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

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(Patient, self).__init__(**kwargs)

    def chameleon_dict(self):
        return {
            "chameleon_id": self.chameleon_id,
            "id_": self.id_,
            "name": self.name,
            "age": self.age,
            "birthdate": self.birthdate,
            "complaint": self.complaint,
            "admission": self.admission.dict(),
            "esi": self.esi.dict(),
        }

    def internal_dict(self):
        return {
            "severity": Severity(value=self.severity.value, at=self.severity.at).dict(),
        }
