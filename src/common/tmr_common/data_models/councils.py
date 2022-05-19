from enum import Enum
from typing import Optional
from pydantic import BaseModel
from tmr_common.data_models.notification import NotificationLevel


class Councils(BaseModel):
    external_id: str
    patient_id: int
    doctor_name: str
    doctor_id: str
    council_name: str
    at: str
    council_date: str
    arrived: Optional[bool]

    class Config:
        orm_mode = True
        use_enum_values = True
        # TODO add the flag to all classes that using enum
