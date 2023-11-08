from typing import List, Dict

from .base import Diffable


class ProtocolItem(Diffable):
    keys: List[str] = []
    key: str
    name: str
    default: str

    def match(self, key):
        return key in self.keys


class ProtocolValue(Diffable):
    value: str
    at: str


class Protocol(Diffable):
    active: bool = False
    items: List[ProtocolItem] = []
    values: Dict[str, ProtocolValue] = {}

    async def match_protocol(self, key, value, at):
        for item in self.items:
            if item.match(key) and (item.key not in self.values or self.values[item.key].at < at):
                self.values[item.key] = ProtocolValue(value=value, at=at)
