import datetime
from enum import Enum
from typing import Optional, List

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
    is_valid: bool
    at: str
    minimum: float
    maximum: float
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
            deps = ([systolic.at_] if systolic else []) + ([diastolic.at_] if diastolic else [])
            kwargs['at'] = min(deps).isoformat() if deps else None
        super(Pressure, self).__init__(**kwargs)


class Latest(BaseModel):
    value: str
    at: str
    is_valid: bool

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at)

    class Config:
        orm_mode = True


class Measures(BaseModel):
    blood_pressure: Optional[Latest]
    systolic: Optional[Latest]
    diastolic: Optional[Latest]
    pulse: Optional[Latest]
    temperature: Optional[Latest]
    saturation: Optional[Latest]

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        systolic = Latest(**kwargs['systolic']) if kwargs.get('systolic') else None
        diastolic = Latest(**kwargs['diastolic']) if kwargs.get('diastolic') else None
        if systolic or diastolic:
            kwargs['blood_pressure'] = Latest(
                value=f"{systolic.value if systolic else '?'}/{diastolic.value if diastolic else '?'}",
                is_valid=(not systolic or systolic.is_valid) and (not diastolic or diastolic.is_valid),
                at=min(([systolic.at_] if systolic else []) + ([diastolic.at_] if diastolic else [])).isoformat()
            )
        super(Measures, self).__init__(**kwargs)


class FullMeasures(BaseModel):
    blood_pressure: List[List[float]]
    pulse: List[List[float]]
    temperature: List[List[float]]
    saturation: List[List[float]]

    class Config:
        orm_mode = True

    def __init__(self, measures=None, **kwargs):
        res = {}
        for measure in measures or []:
            match measure.type:
                case MeasureTypes.pulse.value:
                    res.setdefault(MeasureTypes.pulse.value, []).append([measure.at_.timestamp(), int(measure.value)])
                case MeasureTypes.temperature.value:
                    res.setdefault(MeasureTypes.temperature.value, []).append([measure.at_.timestamp(), measure.value])
                case MeasureTypes.saturation.value:
                    res.setdefault(MeasureTypes.saturation.value, []).append(
                        [measure.at_.timestamp(), int(measure.value)])
                case MeasureTypes.systolic.value:
                    res.setdefault(MeasureTypes.systolic.value, {}).__setitem__(measure.at_.timestamp(),
                                                                                int(measure.value))
                case MeasureTypes.diastolic.value:
                    res.setdefault(MeasureTypes.diastolic.value, {}).__setitem__(measure.at_.timestamp(),
                                                                                 int(measure.value))
        if 'blood_pressure' not in kwargs:
            systolic, diastolic = res.get(MeasureTypes.systolic.value, {}), res.get(MeasureTypes.diastolic.value, {})
            diastolic_keys = iter(sorted(diastolic))
            diastolic_at = next(diastolic_keys, None)
            for t in sorted(systolic):
                while diastolic_at and diastolic_at <= t:
                    res.setdefault(MeasureTypes.blood_pressure.value, []).append(
                        [diastolic_at, systolic[t], diastolic[diastolic_at]]
                    )
                    diastolic_at = next(diastolic_keys, None)
            kwargs['blood_pressure'] = res.get(MeasureTypes.blood_pressure.value, [])
        if 'pulse' not in kwargs:
            kwargs['pulse'] = res.get(MeasureTypes.pulse.value, [])
        if 'temperature' not in kwargs:
            kwargs['temperature'] = res.get(MeasureTypes.temperature.value, [])
        if 'saturation' not in kwargs:
            kwargs['saturation'] = res.get(MeasureTypes.saturation.value, [])
        super(FullMeasures, self).__init__(**kwargs)
