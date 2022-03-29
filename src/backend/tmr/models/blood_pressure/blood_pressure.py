from pydantic import BaseModel
from data_models.measures.blood_pressure.systolic import Systolic
from data_models.measures.blood_pressure.dyastolic import Dyastolic


class BloodPressure(BaseModel):
    dyastolic: Dyastolic
    systolic: Systolic

    class Config:
        orm_mode = True
        json_encoders = {
            Dyastolic: lambda pressure: {"is_valid": {pressure.min <= pressure.value <= pressure.max}, },
            Systolic: lambda pressure: {"is_valid": {pressure.min <= pressure.value <= pressure.max}, },
        }
