from typing import Optional, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from .severity import Severity
from .measures.measures import Measures
from json import loads


class Patient(BaseModel):
    oid: Optional[str] = Field(default_factory=ObjectId)
    name: Optional[str]
    age: Optional[str]
    complaint: Optional[str]
    awaiting: Optional[str]
    flagged: Optional[bool] = False
    measures: Optional[Measures]
    severity: Optional[Severity]
    wing: Optional[str] = Field(default_factory=ObjectId)
    bed: Optional[str]
    warnings: Optional[List[dict]]

    class Config:
        orm_mode = True
        json_encoders = {
            Measures: lambda measures: loads(measures.json(models_as_dict=False)),
        }
