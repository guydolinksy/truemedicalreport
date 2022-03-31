from pydantic import BaseModel
from .blood_pressure.blood_pressure import BloodPressure
from data_models.measures.temperature import Temperature
from data_models.measures.pulse import Pulse


class Measures(BaseModel):
    temperature: Temperature
    blood_pressure: BloodPressure
    pulse: Pulse

    class Config:
        orm_mode = True
        json_encoders = {
            BloodPressure: lambda pressure: {"value": f"{pressure.systolic.value}/{pressure.dyastolic.value}",
                                             "is_valid": {
                                                 pressure.systolic.is_valid and pressure.dyastolic.is_valid},
                                             "time": {
                                                 pressure.systolic.time if pressure.systolic.time < pressure.dyastolic.time else pressure.dyastolic.time},
                                             "is_live": {pressure.systolic.is_live and pressure.dyastolic.is_live}},
            Temperature: lambda temperature: {"value": {temperature.value},
                                              "is_valid": {temperature.min <= temperature.value <= temperature.max},
                                              "time": {temperature.time}},
            Pulse: lambda pulse: {"value": pulse.value, "is_valid": pulse.min <= pulse.value <= pulse.max,
                                  "time": pulse.time}
        }
