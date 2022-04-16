from typing import Optional, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from .severity import Severity
from .measures.measures import Measures
from json import loads


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]

    class Config:
        orm_mode = True


class Patient(BaseModel):
    oid: Optional[str] = Field(default_factory=ObjectId)
    name: Optional[str]
    age: Optional[str]
    complaint: Optional[str]
    awaiting: Optional[str]
    flagged: Optional[bool] = False
    measures: Optional[Measures]
    severity: Optional[Severity]
    admission: Optional[Admission]
    warnings: Optional[List[dict]]

    chameleon_id: Optional[str]  # Not currently in DAL
    unit: Optional[str]  # Not currently in DAL

    class Config:
        orm_mode = True
        json_encoders = {
            Measures: lambda measures: loads(measures.json(models_as_dict=False)),
        }
