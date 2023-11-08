from .base import Diffable, ParsableMixin


class Severity(Diffable, ParsableMixin):
    value: int
    at: str

    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        return cls(**value)
