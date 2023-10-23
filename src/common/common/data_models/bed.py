from typing import Optional

from .base import Diffable


class Bed(Diffable):
    patient: Optional[str]

