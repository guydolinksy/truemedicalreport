import datetime
from enum import Enum
from typing import Optional, List, Union, Any

import logbook
from pydantic import BaseModel

# from pydantic.typing import AbstractSetIntStr, MappingIntStrAny, DictStrAny
AbstractSetIntStr, MappingIntStrAny, DictStrAny = Any, Any, Any

logger = logbook.Logger(__name__)


class MeasureType(Enum):
    pain = 'pain'
    pulse = 'pulse'
    temperature = 'temperature'
    saturation = 'saturation'
    systolic = 'systolic'
    diastolic = 'diastolic'
    blood_pressure = 'blood_pressure'
    weight = 'weight'
    urine_output = 'urine_output'
    breaths = 'breaths'
    enriched_saturation = 'enriched_saturation'
    other = 'other'


class Measure(BaseModel):
    external_id: str
    value: Optional[str]
    is_valid: bool
    at: str
    minimum: Optional[float]
    maximum: Optional[float]
    type: MeasureType

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at)

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if 'is_valid' not in kwargs:
            if kwargs['minimum'] and kwargs['value'] and kwargs['maximum']:
                try:
                    kwargs['is_valid'] = kwargs['minimum'] <= float(kwargs['value']) <= kwargs['maximum']
                except (TypeError, ValueError):
                    kwargs['is_valid'] = False
            else:
                kwargs['is_valid'] = True
        super(Measure, self).__init__(**kwargs)


class Pain(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureType.pain
        super(Pain, self).__init__(**kwargs)


class Pulse(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureType.pulse
        super(Pulse, self).__init__(**kwargs)


class Temperature(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureType.temperature
        super(Temperature, self).__init__(**kwargs)


class Saturation(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureType.saturation
        super(Saturation, self).__init__(**kwargs)


class Systolic(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureType.systolic
        super(Systolic, self).__init__(**kwargs)


class Diastolic(Measure):
    def __init__(self, **kwargs):
        kwargs['type'] = MeasureType.diastolic
        super(Diastolic, self).__init__(**kwargs)


class Pressure(Measure):
    value: str
    minimum: str
    maximum: str

    def __init__(self, systolic: Systolic = None, diastolic: Diastolic = None, **kwargs):
        kwargs['type'] = MeasureType.blood_pressure
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


class Effect(Enum):
    raise_value = 'raise'
    lower_value = 'lower'


class ExpectedEffect(BaseModel):
    measure: MeasureType
    kind: Effect

    class Config:
        orm_mode = True
        use_enum_values = True


class MeasureEffect(BaseModel):
    kind: Optional[Effect]
    label: Optional[str]
    at: Optional[str]

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at) if self.at else None

    class Config:
        orm_mode = True
        use_enum_values = True


class Latest(BaseModel):
    value: Optional[str]
    at: Optional[str]
    is_valid: Optional[bool]
    effect: MeasureEffect = MeasureEffect()

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

    def get(self, kind: MeasureType):
        match kind:
            case MeasureType.pain:
                return self.pain
            case MeasureType.pulse:
                return self.pulse
            case MeasureType.blood_pressure:
                return self.blood_pressure
            case MeasureType.saturation:
                return self.saturation
            case MeasureType.temperature:
                return self.temperature

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
                case MeasureType.pain.value:
                    res.setdefault(MeasureType.pain.value, []).append([measure.at_.timestamp(), measure.value])
                case MeasureType.pulse.value:
                    res.setdefault(MeasureType.pulse.value, []).append([measure.at_.timestamp(), measure.value])
                case MeasureType.temperature.value:
                    res.setdefault(MeasureType.temperature.value, []).append([measure.at_.timestamp(), measure.value])
                case MeasureType.saturation.value:
                    res.setdefault(MeasureType.saturation.value, []).append(
                        [measure.at_.timestamp(), measure.value])
                case MeasureType.systolic.value:
                    res.setdefault(MeasureType.systolic.value, {}).__setitem__(measure.at_.timestamp(),
                                                                               measure.value)
                case MeasureType.diastolic.value:
                    res.setdefault(MeasureType.diastolic.value, {}).__setitem__(measure.at_.timestamp(),
                                                                                measure.value)
        if 'blood_pressure' not in kwargs:
            systolic, diastolic = res.get(MeasureType.systolic.value, {}), res.get(MeasureType.diastolic.value, {})
            diastolic_keys = iter(sorted(diastolic))
            diastolic_at = next(diastolic_keys, None)
            for t in sorted(systolic):
                while diastolic_at and diastolic_at <= t:
                    res.setdefault(MeasureType.blood_pressure.value, []).append(
                        [diastolic_at, systolic[t], diastolic[diastolic_at]]
                    )
                    diastolic_at = next(diastolic_keys, None)
            kwargs['blood_pressure'] = res.get(MeasureType.blood_pressure.value, [])
        if 'pain' not in kwargs:
            kwargs['pain'] = res.get(MeasureType.pain.value, [])
        if 'pulse' not in kwargs:
            kwargs['pulse'] = res.get(MeasureType.pulse.value, [])
        if 'temperature' not in kwargs:
            kwargs['temperature'] = res.get(MeasureType.temperature.value, [])
        if 'saturation' not in kwargs:
            kwargs['saturation'] = res.get(MeasureType.saturation.value, [])
        super(FullMeasures, self).__init__(**kwargs)
