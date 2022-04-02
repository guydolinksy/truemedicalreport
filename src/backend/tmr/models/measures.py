from pydantic import BaseModel
from .blood_pressure.blood_pressure import BloodPressure
from tmr_common.data_models.measures.temperature import Temperature
from tmr_common.data_models.measures.pulse import Pulse


class Measures(BaseModel):
    temperature: Temperature
    blood_pressure: BloodPressure
    pulse: Pulse

    class Config:
        orm_mode = True
        json_encoders = {
            BloodPressure: lambda pressure: {
                "value": f"{pressure.systolic.value}/{pressure.diastolic.value}",
                "is_valid": pressure.systolic.is_valid and pressure.diastolic.is_valid,
                "time": min(pressure.systolic.time, pressure.diastolic.time),
                "is_live": pressure.systolic.is_live and pressure.diastolic.is_live
            },
            Temperature: lambda temperature: {
                "value": temperature.value,
                "is_valid": temperature.min <= temperature.value <= temperature.max,
                "time": temperature.time
            },
            Pulse: lambda pulse: {
                "value": pulse.value,
                "is_valid": pulse.min <= pulse.value <= pulse.max,
                "time": pulse.time
            }
        }
