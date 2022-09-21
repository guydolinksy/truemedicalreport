import datetime
from enum import Enum
from typing import Optional, List, Union, Any

import logbook
from pydantic import BaseModel

# from pydantic.typing import AbstractSetIntStr, MappingIntStrAny, DictStrAny
AbstractSetIntStr, MappingIntStrAny, DictStrAny = Any, Any, Any

logger = logbook.Logger(__name__)


class MeasureTypes(Enum):
    pain = 'pain'
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


class Pain(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureTypes.pain
        super(Pain, self).__init__(**kwargs)


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


class AffectType(Enum):
    raise_value = 'raise'
    lower_value = 'lower'


class Affect(BaseModel):
    kind: Optional[AffectType]
    label: Optional[str]
    at: Optional[str]


class Latest(BaseModel):
    value: Optional[str]
    at: Optional[str]
    is_valid: Optional[bool]
    affect: Affect = Affect()

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at) if self.at else None

    class Config:
        orm_mode = True
        use_enum_values = True


class Measures(BaseModel):

    @classmethod
    def get_properties(cls):
        return [prop for prop in dir(cls) if
                isinstance(getattr(cls, prop), property) and prop not in ("__values__", "fields")]

    def dict(
            self,
            *,
            include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
            exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> DictStrAny:
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        for prop in props:
            value = getattr(self, prop)
            attribs[prop] = value if not isinstance(value, BaseModel) else value.dict(
                by_alias=by_alias,
                skip_defaults=skip_defaults,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            )

        return attribs

    systolic: Latest = Latest()
    diastolic: Latest = Latest()
    pain: Latest = Latest()
    pulse: Latest = Latest()
    temperature: Latest = Latest()
    saturation: Latest = Latest()

    @property
    def blood_pressure(self):
        return Latest(
            value=f"{self.systolic.value or '?'}/{self.diastolic.value or '?'}" \
                if self.systolic.value or self.diastolic.value else None,
            is_valid=self.systolic.is_valid and self.diastolic.is_valid \
                if self.systolic.is_valid or self.diastolic.is_valid else None,
            at=min(filter(None, [self.systolic.at_, self.diastolic.at_])).isoformat() \
                if self.systolic.at_ or self.diastolic.at_ else None
        )

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        super(Measures, self).__init__(**kwargs)


class FullMeasures(BaseModel):
    blood_pressure: List[List[float]]
    pulse: List[List[float]]
    pain: List[List[float]]
    temperature: List[List[float]]
    saturation: List[List[float]]

    class Config:
        orm_mode = True

    def __init__(self, measures=None, **kwargs):
        res = {}
        for measure in measures or []:
            match measure.type:
                case MeasureTypes.pain.value:
                    res.setdefault(MeasureTypes.pain.value, []).append([measure.at_.timestamp(), int(measure.value)])
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
        if 'pain' not in kwargs:
            kwargs['pain'] = res.get(MeasureTypes.pain.value, [])
        if 'pulse' not in kwargs:
            kwargs['pulse'] = res.get(MeasureTypes.pulse.value, [])
        if 'temperature' not in kwargs:
            kwargs['temperature'] = res.get(MeasureTypes.temperature.value, [])
        if 'saturation' not in kwargs:
            kwargs['saturation'] = res.get(MeasureTypes.saturation.value, [])
        super(FullMeasures, self).__init__(**kwargs)
