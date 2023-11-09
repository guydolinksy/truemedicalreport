from typing import Optional

from .base import Diffable


class Person(Diffable):
    id_: str
    name: str
    age: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    phone: Optional[str] = None
