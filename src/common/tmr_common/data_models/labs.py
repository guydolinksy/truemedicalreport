from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

from tmr_common.data_models.notification import LabsNotification


class LabCategories(Enum):
    completeBloodCount = 1001
    gases = 1020
    biochemistry = 1050
    coagulation = 1080


class LabStatus(Enum):
    ordered = 1
    collected = 2
    analyzed = 3


CategoriesInHebrew = {
    LabCategories.completeBloodCount.value: "ספירת תאים",
    LabCategories.gases.value: "בדיקת גזים",
    LabCategories.biochemistry.value: "ביוכימיה",
    LabCategories.coagulation.value: "תפקודי קרישה",
}

StatusInHebrew = {
    LabStatus.ordered.value: "הוזמן",
    LabStatus.collected.value: "שויכו דגימות",
    LabStatus.analyzed.value: "תוצאות",
}

LabTestType = {
    LabCategories.completeBloodCount: ["wbc", "rbc", "leukocytes", "neutrophils"],
    LabCategories.gases: ["pCO2", "pO2"],
    LabCategories.biochemistry: ["troponin", "pH"],
    LabCategories.coagulation: ["pt", "ptt", "d-dimer"],
}


class LabTest(BaseModel):
    external_id: str
    at: str
    test_type_id: int
    test_type_name: str
    category_id: int
    category_name: str
    test_tube_id: Optional[int]
    panic_min_warn_bar: Optional[float]
    min_warn_bar: Optional[float]
    max_warn_bar: Optional[float]
    panic_max_warn_bar: Optional[float]
    result: Optional[float]
    status: LabStatus

    @property
    def category_key(self):
        return self.at, self.category_id

    class Config:
        orm_mode = True
        use_enum_values = True


class LabCategory(BaseModel):
    at: str
    category_id: str
    category: str
    status: str = StatusInHebrew[LabStatus.ordered.value]
    results: Dict[str, LabTest] = {}

    @property
    def key(self):
        return self.at, self.category_id

    @property
    def query_key(self):
        return {'at': self.at, 'category_id': self.category_id}

    class Config:
        orm_mode = True
        use_enum_values = True
