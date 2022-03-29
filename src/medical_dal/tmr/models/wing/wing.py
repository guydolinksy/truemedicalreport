from pydantic import BaseModel
from .isle import Isle


class Wing(BaseModel):
    name: str
    blocks: list[Isle]
