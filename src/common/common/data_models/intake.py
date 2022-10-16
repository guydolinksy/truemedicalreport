from typing import Optional

from pydantic import BaseModel


class Intake(BaseModel):
    complaint: Optional[str]
    nurse_description: Optional[str]
    nurse_seen_time: Optional[str]
    doctor_seen_time: Optional[str]
