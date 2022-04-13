from pydantic import BaseModel
from datetime import datetime


class ESIScore(BaseModel):
    value: int
    time: datetime
    min: int
    max: int

    class Config:
        orm_mode = True