from pydantic import BaseModel, Field
from typing import Optional
from data_models.measures.measures import Measures
from data_models.py_objectid import PyObjectId
from bson.objectid import ObjectId


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
