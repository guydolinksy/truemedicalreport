from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class LabsCategories(Enum):
    completeBloodCount = 'cbc'
    gases = "gases"
    biochemistry = "biochemistry"
    coagulation = "coagulation"


class StatusOfPatientTest(Enum):
    working = "working"
    finished = "finished"


CategoriesInHebrew = {
    LabsCategories.completeBloodCount: "ספירת דם מלאה",
    LabsCategories.gases: "גזים",
    LabsCategories.biochemistry: "ביוכימיה",
    LabsCategories.coagulation: "תפקודי קרישה",
}

LabTestType = {
    LabsCategories.completeBloodCount: ["wbc", "rbc", "leukocytes", "neutrophils"],
    LabsCategories.gases: ["pCO2", "pO2"],
    LabsCategories.biochemistry: ["troponin", "pH"],
    LabsCategories.coagulation: ["pt", "ptt", "d-dimer"],
}


class LabTest(BaseModel):
    category_id: Optional[str]
    category_name: Optional[str]
    test_type_name: Optional[str]
    test_tube_id: Optional[str]
    result: Optional[str]
    min_warn_bar: Optional[float]
    panic_min_warn_bar: Optional[float]
    max_warn_bar: Optional[float]
    panic_max_warn_bar: Optional[float]
    at: Optional[str]

    class Config:
        orm_mode = True


class Labs(BaseModel):
    patient_id: Optional[str]
    results: list[LabTest]

    # def __init__(self, **kwargs):

# class Lab(BaseModel):
#     at: Optional[datetime]
#     tests: Optional[List[LabTest]]
#
#     class Config:
#         orm_mode = True
