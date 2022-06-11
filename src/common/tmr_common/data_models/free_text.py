from pydantic import BaseModel
from typing import Optional, List


class FreeText(BaseModel):
    patient_id = Optional[int]
    medical_record = Optional[int]
    documenting_date = Optional[str]
    documenting_time = Optional[str]
    unit_name = Optional[str]
    unit = Optional[int]
    medical_text_code = Optional[int]
    medical_text_title = Optional[str]
    medical_text = Optional[str]
    documenting_user = Optional[int]
    source = Optional[str]

    class Config:
        orm_mode = True