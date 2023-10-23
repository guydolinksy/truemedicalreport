from typing import Optional

from .base import Diffable


class Person(Diffable):
    id_: str
    name: str
    age: Optional[str]
    gender: Optional[str]
    birthdate: Optional[str]
    phone: Optional[str]

