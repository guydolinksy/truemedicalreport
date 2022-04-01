from pydantic import BaseModel
from .side import Side
from typing import List, Optional


class Isle(BaseModel):
    name: str
    sides: Optional[List[Side]]

    class Config:
        orm_mode = True
