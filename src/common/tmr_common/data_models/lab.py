from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class LabTestType(BaseModel):
    code: Optional[str]
    name: Optional[str]
    category: Optional[str]

    class Config:
        orm_mode = True


class LabTest(BaseModel):
    value: Optional[float]
    panic_low: Optional[float]
    low: Optional[float]
    high: Optional[float]
    panic_high: Optional[float]
    type: LabTestType

    class Config:
        orm_mode = True


class Lab(BaseModel):
    at: Optional[datetime]
    tests: Optional[List[LabTest]]

    class Config:
        orm_mode = True
