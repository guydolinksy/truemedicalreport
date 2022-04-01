from pydantic import BaseModel
from tmr_common.data_models.measures.blood_pressure.systolic import Systolic
from tmr_common.data_models.measures.blood_pressure.diastolic import Diastolic


class BloodPressure(BaseModel):
    diastolic: Diastolic
    systolic: Systolic

    class Config:
        orm_mode = True
        json_encoders = {
            Diastolic: lambda pressure: {"is_valid": {pressure.min <= pressure.value <= pressure.max},
                                         "value": pressure.value,
                                         "time": pressure.time,
                                         "is_live": pressure.is_live},
            Systolic: lambda pressure: {"is_valid": {pressure.min <= pressure.value <= pressure.max},
                                        "value": pressure.value,
                                        "time": pressure.time,
                                        "is_live": pressure.is_live},
        }
