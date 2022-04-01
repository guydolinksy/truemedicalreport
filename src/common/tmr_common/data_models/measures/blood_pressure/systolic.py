from datetime import datetime

from pydantic import BaseModel


class Systolic(BaseModel):
    value: int
    time: datetime
    is_live: bool
    max: int
    min: int
