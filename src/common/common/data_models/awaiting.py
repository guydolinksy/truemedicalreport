from enum import Enum

from pydantic import BaseModel


class Awaiting(BaseModel):
    subtype: str = 'u'
    name: str = 'u'
    since: str = ''
    limit: int = 30
    status: str = ''
    completed: bool = False

    class Config:
        orm_mode = True
        use_enum_values = True


class AwaitingTypes(Enum):
    doctor = "doctor"
    nurse = "nurse"
    imaging = "imaging"
    laboratory = "laboratory"
    referral = "referral"
