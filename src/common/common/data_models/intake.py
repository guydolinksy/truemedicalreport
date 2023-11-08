from typing import Optional

from .base import Diffable


class Intake(Diffable):
    complaint: Optional[str] = None
    nurse_description: Optional[str] = None
    nurse_seen_time: Optional[str] = None
    doctor_seen_time: Optional[str] = None

