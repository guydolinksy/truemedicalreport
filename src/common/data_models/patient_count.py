from pydantic import BaseModel


class PatientCount(BaseModel):
    patient_count: int


class Config:
    orm_mode = True
