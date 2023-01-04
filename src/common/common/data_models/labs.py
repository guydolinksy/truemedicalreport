from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel

from common.data_models.warnings import PatientWarning
from common.data_models.notification import NotificationLevel, Notification, NotificationType
from .severity import Severity


class LabCategories(Enum):
    completeBloodCount = "CBC"
    gases = "בדיקת גזים"
    biochemistry = "ביוכימיה בדם"
    coagulation = "תפקודי קרישה"
    microscopy = "Microscopy"
    therapeutic_drugs = "Therapeutic  Drugs"
    unknown = "אחר"


class LabStatus(Enum):
    ordered = 1
    collected = 2
    analyzed = 3


CategoriesInHebrew = {
    LabCategories.completeBloodCount.value: "CBC",
    LabCategories.gases.value: "בדיקת גזים",
    LabCategories.biochemistry.value: "ביוכימיה בדם",
    LabCategories.coagulation.value: "תפקודי קרישה",
    LabCategories.microscopy.value: "Microscopy",
    LabCategories.therapeutic_drugs: "Therapeutic  Drugs",
    LabCategories.unknown.value: "אחר",
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
    LabCategories.unknown: []
}


class Laboratory(BaseModel):
    patient_id: str
    external_id: str
    at: str
    test_type_id: int
    test_type_name: str
    category_id: str
    category_name: str
    test_tube_id: Optional[int]
    min_warn_bar: Optional[float]
    max_warn_bar: Optional[float]
    result: Optional[str]
    panic: Optional[bool]
    status: LabStatus

    @property
    def category_key(self):
        return self.at, self.category_id

    class Config:
        orm_mode = True
        use_enum_values = True


class LabsNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {kwargs['type'].value: kwargs['static_id']}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.lab
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(LabsNotification, self).__init__(**kwargs)


class LabCategory(BaseModel):
    at: str
    category_id: str
    category: str
    patient_id: str
    status: str = StatusInHebrew[LabStatus.ordered.value]
    results: Dict[str, Laboratory] = {}

    @property
    def key(self):
        return self.at, self.category_id

    @property
    def query_key(self):
        return {'at': self.at, 'category_id': self.category_id}

    def get_instance_id(self):
        return f'{self.category_id}#{self.at.replace(":", "-").replace(".", "-")}'

    class Config:
        orm_mode = True
        use_enum_values = True

    def to_notification(self) -> [LabsNotification]:
        panic = any(category_data.panic for category_data in self.results.values())
        return LabsNotification(
            static_id=self.get_instance_id(),
            patient_id=self.patient_id,
            at=self.at,
            message=f"התקבלו תוצאות {self.category}",
            link="Add in the future",
            level=NotificationLevel.normal if not panic else NotificationLevel.panic,
        )

    def get_updated_warnings(self, warnings: Dict[str, PatientWarning]):
        for id_, lab in self.results.items():
            key = f"lab#{lab.external_id}"
            if key in warnings and not lab.panic:
                yield key, PatientWarning(**warnings[key].dict(exclude={'acknowledge'}), acknowledge=True)
            elif key not in warnings and lab.panic:
                yield key, PatientWarning(
                    content=f"תוצאת {lab.category_name}-{lab.test_type_name} חריגה: {lab.result}",
                    severity=Severity(value=1, at=lab.at), acknowledge=False)
