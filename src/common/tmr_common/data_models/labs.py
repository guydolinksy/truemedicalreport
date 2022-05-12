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
    test_type_id: Optional[int]
    test_tube_id: Optional[int]
    result: Optional[float]
    min_warn_bar: Optional[float]
    panic_min_warn_bar: Optional[float]
    max_warn_bar: Optional[float]
    panic_max_warn_bar: Optional[float]
    at: Optional[datetime]

    class Config:
        orm_mode = True


class LabsResultsInCategory(BaseModel):
    category_id: str
    category_results: list[LabTest]
    class Config:
        orm_mode = True

class LabsResultsOfPatient(BaseModel):
    patient_id: Optional[int]
    external_id: Optional[int]
    lab_results: Optional[list[LabsResultsInCategory]]

    class Config:
        orm_mode = True

    #TODO: implement!
    def to_notification(self):
        pass