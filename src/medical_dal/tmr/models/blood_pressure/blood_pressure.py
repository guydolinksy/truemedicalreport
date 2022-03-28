from pydantic import BaseModel
from systolic import Systolic
from dyastolic import Dyastolic


class BloodPressure(BaseModel):
    dyastolic: Dyastolic
    systolic: Systolic

    class Config:
        orm_mode = True
        json_encoders = {
            Dyastolic: lambda pressure: {"is_valid": {pressure.min <= pressure.value <= pressure.max}},
            Systolic: lambda pressure: {"is_valid": {pressure.min <= pressure.value <= pressure.max}},
        }
