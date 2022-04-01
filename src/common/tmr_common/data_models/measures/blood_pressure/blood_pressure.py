from pydantic import BaseModel
from tmr_common.data_models.measures.blood_pressure.diastolic import Diastolic
from tmr_common.data_models.measures.blood_pressure.systolic import Systolic


class BloodPressure(BaseModel):
    systolic: Systolic
    diastolic: Diastolic

    class Config:
        orm_mode = True
