from typing import List, Dict

from pydantic import BaseModel


class ProtocolItem(BaseModel):
    key: str
    name: str
    default: str


class ProtocolValue(BaseModel):
    value: str
    at: str


class Protocol(BaseModel):
    active: bool = False
    items: List[ProtocolItem] = list()
    values: Dict[str, ProtocolValue] = dict()
