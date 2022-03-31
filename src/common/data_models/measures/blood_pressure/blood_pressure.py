from pydantic import BaseModel
from data_models.measures.blood_pressure.dyastolic import Dyastolic
from data_models.measures.blood_pressure.systolic import Systolic


class BloodPressure(BaseModel):
    systolic: Systolic
    dyastolic: Dyastolic

    class Config:
        orm_mode = True
