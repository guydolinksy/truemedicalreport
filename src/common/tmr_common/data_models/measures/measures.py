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
