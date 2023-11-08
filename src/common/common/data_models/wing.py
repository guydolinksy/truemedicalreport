from typing import List, Any, Dict
from typing import Optional

from .base import Diffable
from .patient import Patient


class WingDetails(Diffable):
    index: int
    columns: Optional[List[dict]] = None
    rows: Optional[List[dict]] = None
    beds: Optional[List[List[Optional[str]]]] = None


class WingFilter(Diffable):
    key: str
    count: int
    title: str
    icon: str
    duration: Optional[str] = None
    valid: bool = True
    children: List[Any] = []


class WingFilters(Diffable):
    awaiting: List[WingFilter]
    doctors: List[WingFilter]
    treatments: List[WingFilter]
    time_since_arrival: List[WingFilter]
    mapping: Dict[str, List[str]]


class Wing(Diffable):
    key: str
    department: str
    name: str
    details: WingDetails
    filters: WingFilters
    patients: Dict[str, Patient]
    department_patients: Dict[str, Patient]
