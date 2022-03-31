from pydantic import BaseModel, Field
from typing import Optional
from .isle import Isle
from typing import List
from ..py_objectid import PyObjectId
from bson.objectid import ObjectId
from ..patient_count import PatientCount
from data_models.patient import Patient


class Wing(BaseModel):
    oid: Optional[str]
    name: Optional[str]
    blocks: Optional[List[Isle]] = None

    class Config:
        orm_mode = True


class WingOverview(Wing):
    patient_count: Optional[PatientCount]
    waiting_patient: Optional[PatientCount]

    class Config:
        orm_mode = True


class WingSummarize(Wing):
    patients_beds: List[Patient]
    structure: Wing

    class Config:
        orm_mode = True
