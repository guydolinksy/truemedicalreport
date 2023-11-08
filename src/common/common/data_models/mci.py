from typing import Optional, List

from .base import Diffable, ParsableMixin


class MCIListItemValue(Diffable, ParsableMixin):
    key: str
    value: str
    at: str

    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        return cls(**value)


class MCIStringValue(Diffable, ParsableMixin):
    value: str
    at: str

    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        return cls(**value)


class MCIBooleanValue(Diffable, ParsableMixin):
    value: bool
    at: str

    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        return cls(**value)


class MCIResult(Diffable):
    real_date: str
    execution_date: str
    parameter: str
    result: str


class MCI(Diffable):
    occupation: Optional[MCIStringValue] = None
    transport: Optional[MCIStringValue] = None
    diagnosis: List[MCIListItemValue] = []
    pre_hospital_treatment: List[MCIListItemValue] = []
    hospital_treatment: List[MCIListItemValue] = []
    imaging: List[MCIListItemValue] = []
