from pydantic import BaseModel
from .side import Side
from typing import List


class Isle(BaseModel):
    name: str
    sides: List[Side]

    class Config:
        orm_mode = True
