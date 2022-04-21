import datetime
from typing import Optional

from pydantic import BaseModel


class Measurement(BaseModel):
    at: str
    value: float
    minimum: float
    maximum: float

    is_valid: bool

    def __init__(self, **kwargs):
        if 'is_valid' not in kwargs:
            kwargs['is_valid'] = kwargs['minimum'] <= kwargs['value'] <= kwargs['maximum']
        super(Measurement, self).__init__(**kwargs)

    class Config:
        orm_mode = True


class Pulse(Measurement):
    pass


class Temperature(Measurement):
    pass


class Saturation(Measurement):
    pass


class Systolic(Measurement):
    pass


class Diastolic(Measurement):
    pass


class BloodPressure(BaseModel):
    systolic: Systolic
    diastolic: Diastolic

    value: str
    is_valid: bool
    at: str

    def __init__(self, **kwargs):
        if 'value' not in kwargs:
            kwargs['value'] = f"{int(kwargs['systolic'].value)}/{int(kwargs['diastolic'].value)}"
        if 'is_valid' not in kwargs:
            kwargs['is_valid'] = kwargs['systolic'].is_valid and kwargs['diastolic'].is_valid
        if 'at' not in kwargs:
            kwargs['at'] = min(
                map(datetime.datetime.fromisoformat, [kwargs['systolic'].at, kwargs['diastolic'].at])
            ).isoformat()
        super(BloodPressure, self).__init__(**kwargs)


class Measures(BaseModel):
    blood_pressure: Optional[BloodPressure]
    pulse: Optional[Pulse]
    temperature: Optional[Temperature]
    saturation: Optional[Saturation]

    class Config:
        orm_mode = True
