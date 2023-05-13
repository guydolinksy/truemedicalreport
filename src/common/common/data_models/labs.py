from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel

from common.data_models.notification import NotificationLevel, Notification, NotificationType
from common.data_models.warnings import PatientWarning
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


CATEGORIES_IN_HEBREW = {
    LabCategories.completeBloodCount.value: "CBC",
    LabCategories.gases.value: "בדיקת גזים",
    LabCategories.biochemistry.value: "ביוכימיה בדם",
    LabCategories.coagulation.value: "תפקודי קרישה",
    LabCategories.microscopy.value: "Microscopy",
    LabCategories.therapeutic_drugs.value: "Therapeutic  Drugs",
    LabCategories.unknown.value: "אחר",
}

STATUS_IN_HEBREW = {
    LabStatus.ordered.value: "הוזמן",
    LabStatus.collected.value: "שויכו דגימות",
    LabStatus.analyzed.value: "תוצאות",
}

LAB_TEST_TYPE = {
    LabCategories.completeBloodCount.value: ["wbc", "rbc", "leukocytes", "neutrophils"],
    LabCategories.gases.value: ["pCO2", "pO2"],
    LabCategories.biochemistry.value: ["troponin", "pH"],
    LabCategories.coagulation.value: ["pt", "ptt", "d-dimer"],
    LabCategories.therapeutic_drugs.value: [],
    LabCategories.microscopy.value: [],
    LabCategories.unknown.value: []
}


class Laboratory(BaseModel):
    patient_id: str
    external_id: str
    ordered_at: str
    chameleon_id: str
    result_at: Optional[str]
    test_type_id: int
    test_type_name: str
    category_id: str
    category_name: str
    test_tube_id: Optional[int]
    min_warn_bar: Optional[float]
    max_warn_bar: Optional[float]
    result: Optional[str]
    units: Optional[str]
    panic: Optional[bool]
    status: LabStatus

    @property
    def category_key(self):
        return self.ordered_at, self.category_id

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
    ordered_at: str
    result_at: Optional[str]
    category_id: str
    category: str
    patient_id: str
    status: str = STATUS_IN_HEBREW[LabStatus.ordered.value]
    results: Dict[str, Laboratory] = {}

    @property
    def key(self):
        return self.ordered_at, self.category_id

    @property
    def query_key(self):
        return {'at': self.ordered_at, 'category_id': self.category_id}

    def get_instance_id(self):
        return f'{self.patient_id}#{self.category_id}#{self.ordered_at.replace(":", "-").replace(".", "-")}'

    class Config:
        orm_mode = True
        use_enum_values = True

    def to_notifications(self) -> List[LabsNotification]:
        res = []
        for key, result in self.results.items():
            if result.max_warn_bar and self.result_at and float(result.result) > float(result.max_warn_bar):
                res.append(LabsNotification(
                    static_id=f'{self.get_instance_id()}#{key}',
                    patient_id=self.patient_id,
                    at=self.result_at,
                    message=f"תוצאת {self.category}-{result.test_type_name} גבוהה: {result.result} {result.units}",
                    link="Add in the future",
                    level=NotificationLevel.abnormal if not result.panic else NotificationLevel.panic,
                ))
            if result.min_warn_bar and self.result_at and float(result.result) < float(result.min_warn_bar):
                res.append(LabsNotification(
                    static_id=f'{self.get_instance_id()}#{key}',
                    patient_id=self.patient_id,
                    at=self.result_at,
                    message=f"תוצאת {self.category}-{result.test_type_name} נמוכה: {result.result} {result.units}",
                    link="Add in the future",
                    level=NotificationLevel.abnormal if not result.panic else NotificationLevel.panic,
                ))
        return res if res else [LabsNotification(
            static_id=self.get_instance_id(),
            patient_id=self.patient_id,
            at=self.result_at if self.result_at else self.ordered_at,
            message=f"תוצאות {self.category} תקינות",
            link="Add in the future",
            level=NotificationLevel.normal,
        )]

    def get_updated_warnings(self, warnings: Dict[str, PatientWarning]):
        for id_, lab in self.results.items():
            key = f"lab#{lab.external_id}"
            if key in warnings and not lab.panic:
                yield key, PatientWarning(**warnings[key].dict(exclude={'acknowledge'}), acknowledge=True)
            elif key not in warnings and lab.panic:
                yield key, PatientWarning(
                    content=f"תוצאת {lab.category_name}-{lab.test_type_name} חריגה: {lab.result} {lab.units}",
                    severity=Severity(value=1, at=self.result_at if self.result_at else self.ordered_at),
                    acknowledge=False)
