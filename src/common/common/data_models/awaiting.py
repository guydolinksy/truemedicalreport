import datetime
from enum import Enum
from typing import Optional

from .base import Diffable


class Awaiting(Diffable):
    subtype: str
    name: str
    since: str
    limit: int
    status: str
    completed_at: Optional[str] = None

    @property
    def completed_at_(self):
        return datetime.datetime.fromisoformat(self.completed_at) if self.completed_at else None


class AwaitingTypes(str, Enum):
    doctor = "doctor"
    nurse = "nurse"
    imaging = "imaging"
    laboratory = "laboratory"
    referral = "referral"
