import datetime
from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel

from common.data_models.notification import NotificationLevel, Notification, NotificationType
from common.data_models.warnings import PatientWarning
from .severity import Severity


class LabStatus(Enum):
    ordered = 1
    collected = 2
    in_progress = 3
    analyzed = 4


CATEGORIES_IN_HEBREW = {
    "Therapeutic  Drugs": "Therapeutic Drugs",
}
#
# LAB_TEST_TYPE = {
#     LabCategories.completeBloodCount.value: ["wbc", "rbc", "leukocytes", "neutrophils"],
#     LabCategories.gases.value: ["pCO2", "pO2"],
#     LabCategories.biochemistry.value: ["troponin", "pH"],
#     LabCategories.coagulation.value: ["pt", "ptt", "d-dimer"],
#     LabCategories.therapeutic_drugs.value: [],
#     LabCategories.microscopy.value: [],
#     LabCategories.unknown.value: []
# }


class Laboratory(BaseModel):
    patient_id: str
    external_id: str
    ordered_at: str
    chameleon_id: Optional[str]
    result_at: Optional[str]
    test_type_id: int
    test_type_name: str
    category: str
    category_display_name: str
    result: Optional[str]
    units: Optional[str]
    range: Optional[str]
    panic: Optional[bool]
    status: LabStatus

    @property
    def category_key(self):
        return self.ordered_at, self.category

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
    category: str
    category_display_name: str
    patient_id: str
    status: str = LabStatus.ordered.value
    results: Dict[str, Laboratory] = {}

    @property
    def key(self):
        return f"{self.category}-{self.ordered_at.replace('.', '-').replace(':', '-')}"

    @property
    def query_key(self):
        return {'at': self.ordered_at, 'category': self.category}

    def get_instance_id(self):
        return f'{self.patient_id}#{self.category}#{self.ordered_at}'.\
            replace(":", "-").replace(".", "-").replace("+", "-")

    class Config:
        orm_mode = True
        use_enum_values = True

    def to_notifications(self) -> List[LabsNotification]:
        res = []
        out_of_range = False
        for key, result in self.results.items():
            if not result.range or result.range == 'N':
                continue
            out_of_range = True
            if result.range == 'VH' or result.range == 'PH':
                res.append(LabsNotification(
                    static_id=f'{self.get_instance_id()}#{key}',
                    patient_id=self.patient_id,
                    at=result.result_at,
                    message=f"תוצאת {self.category}-{result.test_type_name} גבוהה: {result.result} {result.units}",
                    link=None,  # TODO "Add in the future",
                    level=NotificationLevel.abnormal if not result.range == 'PH' else NotificationLevel.panic,
                ))
            if result.range == 'VL' or result.range == 'PL':
                res.append(LabsNotification(
                    static_id=f'{self.get_instance_id()}#{key}',
                    patient_id=self.patient_id,
                    at=result.result_at,
                    message=f"תוצאת {self.category}-{result.test_type_name} נמוכה: {result.result} {result.units}",
                    link=None,  # "Add in the future",
                    level=NotificationLevel.abnormal if not result.range == 'PL' else NotificationLevel.panic,
                ))
        return res if res else [LabsNotification(
            static_id=self.get_instance_id(),
            patient_id=self.patient_id,
            at=max(datetime.datetime.fromisoformat(l.result_at) for l in self.results.values()).isoformat(),
            message=f"תוצאות {self.category} {'לא ' if out_of_range else ''}תקינות",
            link=None,  # "Add in the future",
            level=NotificationLevel.abnormal if out_of_range else NotificationLevel.normal,
        )]

    def get_updated_warnings(self, warnings: Dict[str, PatientWarning]):
        for id_, lab in self.results.items():
            key = f"lab#{lab.external_id}"
            if key in warnings and not lab.panic:
                yield key, PatientWarning(**warnings[key].dict(exclude={'acknowledge'}), acknowledge=True)
            elif key not in warnings and lab.panic:
                yield key, PatientWarning(
                    content=f"תוצאת {lab.category_display_name}-{lab.test_type_name} חריגה: {lab.result} {lab.units}",
                    severity=Severity(value=1, at=lab.result_at),
                    acknowledge=False)
