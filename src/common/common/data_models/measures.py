import datetime
from enum import Enum
from typing import Optional, List, Any, Generic, TypeVar, NamedTuple, Tuple

import logbook
from pydantic import computed_field

from .base import Diffable

# from pydantic.typing import AbstractSetIntStr, MappingIntStrAny, DictStrAny
AbstractSetIntStr, MappingIntStrAny, DictStrAny = Any, Any, Any

logger = logbook.Logger(__name__)


class MeasureType(str, Enum):
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


T = TypeVar('T')


class Value(Diffable, Generic[T]):
    at: str
    value: T
    minimum: Optional[T] = None
    maximum: Optional[T] = None

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at)

    @computed_field
    @property
    def is_valid(self) -> Optional[bool]:
        if self.minimum is not None and self.maximum is not None and self.value is not None:
            try:
                if not isinstance(self.value, tuple):
                    return float(self.minimum) <= float(self.value) <= float(self.maximum)
                for minimum, value, maximum in zip(self.minimum, self.value, self.maximum):
                    if minimum is not None and maximum is not None and value is not None and \
                            not float(minimum) <= float(value) <= float(maximum):
                        return False
                else:
                    return True
            except ValueError:
                return False


class EffectType(str, Enum):
    increase = '+'
    decrease = '-'


class Effect(Diffable):
    at: str
    kind: EffectType
    label: str

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at)


class ExpectedEffect(Diffable):
    measure: MeasureType
    kind: Effect


class DynamicValue(Value[T], Generic[T]):
    effect: Optional[Effect] = None


class Measure(DynamicValue[T], Generic[T]):
    external_id: str
    type: MeasureType


class BP(NamedTuple):
    systolic: str
    diastolic: Optional[str]


class Measures(Diffable):
    systolic: Optional[Value[str]] = None
    diastolic: Optional[Value[str]] = None
    pain: Optional[Value[str]] = None
    pulse: Optional[Value[str]] = None
    temperature: Optional[Value[str]] = None
    saturation: Optional[Value[str]] = None

    @computed_field
    @property
    def blood_pressure(self) -> Optional[Value[BP]]:
        if not self.systolic:
            return None
        if not self.diastolic or self.systolic.at != self.diastolic.at:
            return Value(value=(self.systolic.value, None), at=self.systolic.at,
                         minimum=(self.systolic.minimum, None) if self.systolic.minimum else None,
                         maximum=(self.systolic.maximum, None) if self.systolic.maximum else None)
        return Value(value=(self.systolic.value, self.diastolic.value), at=self.systolic.at,
                     minimum=(self.systolic.minimum, self.diastolic.minimum) if self.systolic.minimum else None,
                     maximum=(self.systolic.maximum, self.diastolic.maximum) if self.systolic.maximum else None)


class FullMeasures(Diffable):
    blood_pressure: List[Tuple[float, float, float]] = []
    pulse: List[Tuple[float, float]] = []
    pain: List[Tuple[float, float]] = []
    temperature: List[Tuple[float, float]] = []
    saturation: List[Tuple[float, float]] = []

    @classmethod
    def from_measures(cls, measures: List[Measure]):
        res = dict(blood_pressure=[], systolic=[], diastolic=[], pulse=[], pain=[], temperature=[], saturation=[])

        for measure in measures:
            if measure.value is not None:
                try:
                    res.get(measure.type, []).append((int(measure.at_.timestamp() * 1000), float(measure.value)))
                except ValueError:
                    logger.exception('Invalid format for measurement {}@{}', measure.type, measure.at_)

        systolic, diastolic = dict(res.pop('systolic')), dict(res.pop('diastolic'))
        if systolic and not diastolic:
            diastolic = {min(systolic): 0}
        diastolic_keys = iter(sorted(diastolic))
        diastolic_at = next(diastolic_keys, None)
        for t in sorted(systolic):
            while diastolic_at and diastolic_at <= t:
                res['blood_pressure'].append((diastolic_at, systolic[t], diastolic[diastolic_at]))
                diastolic_at = next(diastolic_keys, None)

        return cls(**{k: sorted(v) for k, v in res.items()})
