from typing import List, Dict

from .base import Diffable
from .patient import Patient
from .wing import Wing


class Department(Diffable):
    key: str
    name: str
    wings: List[Wing]
    patients: Dict[str, Patient]
