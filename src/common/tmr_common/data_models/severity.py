from pydantic import BaseModel
from datetime import datetime


class Severity(BaseModel):
    value: int
    at: str

    class Config:
        orm_mode = True
