from pydantic import BaseModel
from datetime import datetime


class Severity(BaseModel):
    value: int
    time: datetime

    class Config:
        orm_mode = True
