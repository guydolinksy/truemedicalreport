from typing import Optional

from .base import Diffable


class Admission(Diffable):
    arrival: str
    department_id: str
    wing_id: Optional[str] = None
    bed: Optional[str] = None
