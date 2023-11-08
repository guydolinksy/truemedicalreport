from typing import List, Dict

from .base import Diffable
from .patient import Patient
from .wing import Wing


class PatientEntry(Diffable):
    oid: str
    patient: Patient


class Department(Diffable):
    key: str
    name: str
    shortName: str
    wings: List[Wing]
    patients: List[PatientEntry]
