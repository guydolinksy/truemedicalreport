from enum import Enum

from pydantic import BaseModel


class Awaiting(BaseModel):
    subtype: str
    name: str
    since: str
    limit: int
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
