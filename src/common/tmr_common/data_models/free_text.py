from enum import Enum

from pydantic import BaseModel
from typing import Optional, List

from tmr_common.data_models.patient import BasicMedical


class MedicalCode(Enum):
    doctor = 1
    nurse = 901


class FreeText(BaseModel):
    patient_id: Optional[int]
    medical_record: Optional[int]
    documenting_date: Optional[str]
    documenting_time: Optional[str]
    unit_name: Optional[str]
    unit: Optional[int]
    medical_text_code: MedicalCode
    medical_text_title: Optional[str]
    medical_text: Optional[str]
    documenting_user: Optional[int]
    source: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True




def convert_to_basic_medical(free_text: FreeText):
    if free_text.medical_text in (MedicalCode.doctor, MedicalCode.nurse):
        return BasicMedical(nurse_description=free_text.medical_text,
                            nurse_seen_time=free_text.documenting_time)