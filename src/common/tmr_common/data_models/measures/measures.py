from pydantic import BaseModel
from tmr_common.data_models.measures.pulse import Pulse
from tmr_common.data_models.measures.temperature import Temperature
from tmr_common.data_models.measures.blood_pressure.blood_pressure import BloodPressure


class Measures(BaseModel):
    blood_pressure: BloodPressure
    pulse: Pulse
    temperature: Temperature

    class Config:
        orm_mode = True
        json_encoders = {
            BloodPressure: lambda pressure: {"value": f"{pressure.systolic.value}/{pressure.diastolic.value}",
                                             "is_valid": (
                                                                 pressure.systolic.min <= pressure.systolic.value <= pressure.systolic.max) and
                                                         (
                                                                 pressure.diastolic.min <= pressure.diastolic.value <= pressure.diastolic.max),
                                             "time": min(pressure.systolic.time, pressure.diastolic.time),
                                             "is_live": pressure.systolic.is_live and pressure.diastolic.is_valid},
            Temperature: lambda temperature: {"value": temperature.value,
                                              "is_valid": temperature.min <= temperature.value <= temperature.max,
                                              "time": temperature.time},
            Pulse: lambda pulse: {"value": pulse.value, "is_valid": pulse.min <= pulse.value <= pulse.max,
                                  "time": pulse.time}

        }
