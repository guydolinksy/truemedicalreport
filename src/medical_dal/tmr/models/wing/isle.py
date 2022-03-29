from pydantic import BaseModel
from .side import Side


class Isle(BaseModel):
    name: str
    sides: [Side]
