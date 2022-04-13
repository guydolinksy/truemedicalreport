from typing import Optional, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from .esi_score import ESIScore
from .measures.measures import Measures
from json import loads


class Patient(BaseModel):
    oid: Optional[str] = Field(default_factory=ObjectId)
    name: Optional[str]
    complaint: Optional[str]
    awaiting: Optional[str]
    flagged: Optional[bool] = False
    measures: Optional[Measures]
    esi_score: Optional[ESIScore]
    wing: Optional[str] = Field(default_factory=ObjectId)
    bed: Optional[str]
    warnings: Optional[List[str]]

    cameleon_id : Optional[str] #Not currently in DAL
    unit: Optional[str] #Not currently in DAL
    class Config:
        orm_mode = True
        json_encoders = {
            Measures: lambda measures: loads(measures.json(models_as_dict=False)),
            ESIScore: lambda esi_score: {
                'value': esi_score.value,
                'is_valid': esi_score.min <= esi_score.value <= esi_score.max,
                'time': esi_score.time,
                'min': esi_score.min,
                'max': esi_score.max,
            }
        }
