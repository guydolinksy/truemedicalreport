from pydantic import BaseModel


class Referral(BaseModel):
    external_id: str
    patient_id: int
    to: str
    at: str
    completed: bool = False

    class Config:
        orm_mode = True
