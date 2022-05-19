from typing import Optional

from pydantic import BaseModel


class WaitForDoctor(BaseModel):
    doctor_name: Optional[str]
    patients_waiting: Optional[int]


class MedicalSum(BaseModel):
    waiting_for_doctor: Optional[list[WaitForDoctor]]
    waiting_for_council: Optional[int]

    class Config:
        orm_mode = True
