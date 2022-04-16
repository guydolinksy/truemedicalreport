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
    oid: Optional[str] = Field(default_factory=ObjectId)
    name: Optional[str]
    identification: Optional[str]
    age: Optional[str]
    complaint: Optional[str]
    awaiting: Optional[str]
    flagged: Optional[bool] = False
    measures: Optional[Measures]
    severity: Optional[Severity]
    admission: Optional[Admission]
    warnings: Optional[List[dict]]

    class Config:
        orm_mode = True
