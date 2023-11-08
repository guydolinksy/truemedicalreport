from typing import Optional

from .base import Diffable, ParsableMixin


class Admission(Diffable, ParsableMixin):
    arrival: str
    department_id: str
    wing_id: Optional[str] = None
    bed: Optional[str] = None

    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        return cls(**value)
