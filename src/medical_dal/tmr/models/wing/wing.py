from pydantic import BaseModel
from .isle import Isle
from typing import List


class Wing(BaseModel):
    name: str
    blocks: List[Isle]

    class Config:
        orm_mode = True
