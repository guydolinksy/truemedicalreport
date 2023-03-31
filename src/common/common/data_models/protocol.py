from typing import List, Dict

from pydantic import BaseModel


class ProtocolItem(BaseModel):
    keys: List[str] = list()
    key: str
    name: str
    default: str

    def match(self, key):
        return key in self.keys


class ProtocolValue(BaseModel):
    value: str
    at: str


class Protocol(BaseModel):
    active: bool = False
    items: List[ProtocolItem] = list()
    values: Dict[str, ProtocolValue] = dict()
