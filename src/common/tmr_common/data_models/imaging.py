import datetime
from typing import Optional

from pydantic import BaseModel


class Imaging(BaseModel):
    at: str
    name: float
    value: str
    link: str

    def __init__(self, **kwargs):
        super(Imaging, self).__init__(**kwargs)

    class Config:
        orm_mode = True
