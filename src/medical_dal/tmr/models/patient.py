from pydantic import BaseModel, Field
from data_models.measures.measures import Measures
from py_objectid import PyObjectId


class Patient(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    complaint: str = Field(...)
    awating: str = Field(...)
    flagged: bool = False
    measures: Measures
    esi_score: int
    wing_id: str = None
    bed: str = Field(...)
    warnings: list[str]
