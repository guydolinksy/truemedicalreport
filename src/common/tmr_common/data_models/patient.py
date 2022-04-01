from typing import Optional, List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from .esi_score import ESIScore
from .measures.measures import Measures


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

    class Config:
        orm_mode = True
