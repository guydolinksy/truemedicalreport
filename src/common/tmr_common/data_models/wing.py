from typing import List, Any, Dict
from typing import Optional

from pydantic import BaseModel

from .patient import Patient, PatientNotifications


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


class WingFilter(BaseModel):
    value: str
    title: str
    children: List[Any] = list()

    class Config:
        orm_mode = True


class WingFilters(BaseModel):
    tree: List[WingFilter]
    mapping: Dict[str, List[str]]

    class Config:
        orm_mode = True


class WingSummary(Wing):
    patients: List[Patient]
    details: Wing
    filters: WingFilters
    notifications: List[PatientNotifications]

    class Config:
        orm_mode = True
