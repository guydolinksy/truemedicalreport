from pydantic import BaseModel
from tmr_common.data_models.measures.blood_pressure.dyastolic import Dyastolic
from tmr_common.data_models.measures.blood_pressure.systolic import Systolic


class BloodPressure(BaseModel):
    systolic: Systolic
    dyastolic: Dyastolic

    class Config:
        orm_mode = True
