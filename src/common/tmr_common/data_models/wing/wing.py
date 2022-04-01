from types import NoneType

from pydantic import BaseModel
from typing import Optional
from typing import List
from ..patient_count import PatientCount
from tmr_common.data_models.patient import Patient


class Wing(BaseModel):
    oid: Optional[str]
    name: Optional[str]
    columns: Optional[List[dict]]
    rows: Optional[List[dict]]
    beds: Optional[List[List[Optional[str]]]]

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
