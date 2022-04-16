from pydantic import BaseModel
from datetime import datetime


class Severity(BaseModel):
    value: int
    at: datetime

    class Config:
        orm_mode = True
