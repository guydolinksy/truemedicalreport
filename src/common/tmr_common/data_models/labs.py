from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from tmr_common.data_models.notification import LabsNotification


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
    at: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True


class LabsResultsInCategory(BaseModel):
    category_id: str
    category_results: list[LabTest]

    class Config:
        orm_mode = True
        use_enum_values = True


class LabsResultsOfPatient(BaseModel):
    patient_id: Optional[int]
    external_id: Optional[int]
    lab_results: Optional[list[LabsResultsInCategory]]

    class Config:
        orm_mode = True
        use_enum_values = True

    # TODO: Plan wanted notification
    def to_notification(self):
        return LabsNotification(
            static_id=self.external_id,
            patient_id=self.patient_id,
            at=datetime.now(),
            message = self.get_notification_message()
        )

    def _get_categories_name(self) -> []:
        categories_names = []
        for category_data in self.lab_results:
            categories_names.append(CategoriesInHebrew[LabsCategories[category_data.category_id]])
        return categories_names

    def get_notification_message(self)->str:
        categories_names = self._get_categories_name()
        message = "התקבלו תוצאות מעבדה חדשות ב-"
        for category in categories_names:
            message += f" {category},"
        return message
