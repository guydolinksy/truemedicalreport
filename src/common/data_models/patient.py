from pydantic import BaseModel, Field
from typing import Optional
from data_models.measures.measures import Measures
from bson.objectid import ObjectId
from json import loads


class Patient(BaseModel):
    oid: Optional[str] = Field(default_factory=ObjectId)
    name: Optional[str]
    complaint: Optional[str]
    awating: Optional[str]
    flagged: Optional[bool] = False
    measures: Optional[Measures]
    esi_score: Optional[int]
    wing: Optional[str] = Field(default_factory=ObjectId)
    bed: Optional[str]
    warnings: Optional[list[str]]

    class Config:
        orm_mode = True
        json_encoders = {
            Measures: lambda measures: loads(measures.json(models_as_dict=False))
        }
