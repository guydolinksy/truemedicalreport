from pydantic import BaseModel
from datetime import datetime


class Pulse(BaseModel):
    value: int
    time: datetime
    min: int
    max: int
