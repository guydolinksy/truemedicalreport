from .base import Diffable
from .severity import Severity


class PatientWarning(Diffable):
    content: str
    severity: Severity
    acknowledge: bool = False
