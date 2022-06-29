from typing import List
from typing import Optional

from pydantic import BaseModel

from tmr_common.data_models.patient import Patient


class Wing(BaseModel):
    oid: Optional[str]
    name: Optional[str]
    key: Optional[str]
    department: Optional[str]
    columns: Optional[List[dict]]
    rows: Optional[List[dict]]
    beds: Optional[List[List[Optional[str]]]]

    class Config:
        orm_mode = True


class WingOverview(Wing):
    patient_count: Optional[int]
    waiting_patient: Optional[int]

    class Config:
        orm_mode = True


class WingSummary(Wing):
    patients: List[Patient]
    details: Wing

    class Config:
        orm_mode = True
