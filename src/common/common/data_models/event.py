from .base import Diffable


class Event(Diffable):
    key: str
    content: str
    at: str
