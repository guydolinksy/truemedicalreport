import datetime
from enum import Enum
from typing import Optional

import logbook
from pydantic import BaseModel

logger = logbook.Logger(__name__)


class MeasureTypes(Enum):
    pulse = 'pulse'
    temperature = 'temperature'
    saturation = 'saturation'
    systolic = 'systolic'
    diastolic = 'diastolic'
    blood_pressure = 'blood_pressure'


class Measure(BaseModel):
    external_id: str
    value: float
    minimum: float
    maximum: float
    is_valid: bool
    at: str
    type: MeasureTypes

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at)

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if 'is_valid' not in kwargs:
            kwargs['is_valid'] = kwargs['minimum'] <= kwargs['value'] <= kwargs['maximum']
        super(Measure, self).__init__(**kwargs)


class Pulse(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureTypes.pulse
        super(Pulse, self).__init__(**kwargs)


class Temperature(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureTypes.temperature
        super(Temperature, self).__init__(**kwargs)


class Saturation(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureTypes.saturation
        super(Saturation, self).__init__(**kwargs)


class Systolic(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureTypes.systolic
        super(Systolic, self).__init__(**kwargs)


class Diastolic(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureTypes.diastolic
        super(Diastolic, self).__init__(**kwargs)


class Pressure(Measure):
    value: str
    minimum: str
    maximum: str

    def __init__(self, systolic: Systolic = None, diastolic: Diastolic = None, **kwargs):
        kwargs['type'] = MeasureTypes.blood_pressure
        if 'external_id' not in kwargs:
            kwargs['external_id'] = f"{systolic.external_id if systolic else '?'}#" \
                                    f"{diastolic.external_id if diastolic else '?'}"
        if 'value' not in kwargs:
            kwargs['value'] = f"{int(systolic.value) if systolic else '?'}/" \
                              f"{int(diastolic.value) if diastolic else '?'}"
        if 'minimum' not in kwargs:
            kwargs['minimum'] = f"{int(systolic.minimum) if systolic else '?'}/" \
                                f"{int(diastolic.minimum) if diastolic else '?'}"
        if 'maximum' not in kwargs:
            kwargs['maximum'] = f"{int(systolic.maximum) if systolic else '?'}/" \
                                f"{int(diastolic.maximum) if diastolic else '?'}"
        if 'is_valid' not in kwargs:
            kwargs['is_valid'] = (not systolic or systolic.is_valid) and (not diastolic or diastolic.is_valid)
        if 'at' not in kwargs:
            deps = ([systolic.at] if systolic else []) + ([diastolic.at] if diastolic else [])
            kwargs['at'] = min(map(datetime.datetime.fromisoformat, deps)).isoformat() if deps else None
        super(Pressure, self).__init__(**kwargs)


class Measures(BaseModel):
    systolic: Optional[Systolic]
    diastolic: Optional[Diastolic]
    pulse: Optional[Pulse]
    temperature: Optional[Temperature]
    saturation: Optional[Saturation]

    class Config:
        orm_mode = True
