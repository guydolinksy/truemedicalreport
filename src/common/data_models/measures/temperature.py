from pydantic import BaseModel
from datetime import datetime


class Temperature(BaseModel):
    value: float
    time: datetime
    is_live: bool
    min: float
    max: float
