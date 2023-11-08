import datetime
from enum import Enum
from typing import Optional, Dict

from pydantic import computed_field

from .base import Diffable
from .notification import NotificationLevel, Notification, NotificationType
from .severity import Severity
from .warnings import PatientWarning


class LabStatus(int, Enum):
    ordered = 1
    collected = 2
    in_progress = 3
    analyzed = 4


# LABS_RESULT_RANGE = {
#     # WBC
#     100109500: {"min": 3, "max": 14},
#     # HBG
#     100109497: {"min": 8, "max": 16},
#     # PLT
#     100109488: {"min": 150, "max": 500},
#     # EOS%
#     100109478: {"min": 0, "max": 1},
#     # EOS abs
#     # 100109477: {"min": 1, "max": 1000},
#     # NEUTRO%
#     100109484: {"min": 1, "max": 10},
#     # NEUTRO abs
#     # 100109483: {"min": 1, "max": 10}
# }
#

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


class Laboratory(Diffable):
    ordered_at: str
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

    @computed_field
    @property
    def external_id(self) -> str:
        return f"{self.test_type_id}"

    @property
    def result_at_(self):
        return datetime.datetime.fromisoformat(self.result_at) if self.result_at else None


class LabsNotification(Notification):
    type_: NotificationType = NotificationType.lab


class LabCategory(Diffable):
    ordered_at: str
    category: str
    category_display_name: str
    status: LabStatus = LabStatus.ordered
    results: Dict[str, Laboratory] = {}

    @computed_field
    @property
    def external_id(self) -> str:
        return f"{self.category}-{self.ordered_at.replace('.', '-').replace(':', '-').replace('+', '-')}"

    @property
    def query_key(self):
        return {'at': self.ordered_at, 'category': self.category}

    def to_notifications(self) -> Dict[str, LabsNotification]:
        res = {}
        out_of_range = False
        fault_laboratory = False
        for key, result in self.results.items():
            # if result.result and result.test_type_id in LABS_RESULT_RANGE:
            #     try:
            #         lab_result = int(result.result)
            #         if not LABS_RESULT_RANGE[result.test_type_id]["min"] < lab_result < \
            #                LABS_RESULT_RANGE[result.test_type_id]["max"]:
            #             out_of_range = True
            #     except ValueError:
            #         continue
            if result.range == 'X':
                fault_laboratory = True
                continue
            elif not result.range or result.range == 'N':
                continue
            out_of_range = True
            # TODO decide if the special labs needs to be VH or HH or VL, LL
            if result.range == 'VH' or result.range == 'HH':
                l = LabsNotification(
                    static_id=f'{self.external_id}#{key}',
                    at=result.result_at,
                    message=f"{result.test_type_name} גבוה: {result.result} {result.units}",
                    link=None,  # TODO "Add in the future",
                    level=NotificationLevel.abnormal if not result.range == 'HH' else NotificationLevel.panic,
                )
                res[l.static_id] = l
            if result.range == 'VL' or result.range == 'LL':
                l = LabsNotification(
                    static_id=f'{self.external_id}#{key}',
                    at=result.result_at,
                    message=f"{result.test_type_name} נמוך: {result.result} {result.units}",
                    link=None,  # "Add in the future",
                    level=NotificationLevel.abnormal if not result.range == 'LL' else NotificationLevel.panic,
                )
                res[l.static_id] = l
        if res:
            return res
        if self.status != LabStatus.analyzed or not fault_laboratory:
            return {}
        l = LabsNotification(
            static_id=self.external_id,
            at=max(datetime.datetime.fromisoformat(l.result_at) for l in self.results.values()).isoformat(),
            message=f"{self.category} פסול",
            link=None,  # "Add in the future",
            level=NotificationLevel.abnormal if out_of_range else NotificationLevel.normal,
        )

        return {l.static_id: l}

    def get_updated_warnings(self, warnings: Dict[str, PatientWarning]):
        for id_, lab in self.results.items():
            key = f"lab#{lab.external_id}"
            if key in warnings and not lab.panic:
                yield key, PatientWarning(**warnings[key].dict(exclude={'acknowledge'}), acknowledge=True)
            elif key not in warnings and lab.range in ['HH', 'LL']:
                yield key, PatientWarning(
                    content=f"{lab.test_type_name} חריג: {lab.result} {lab.units}",
                    severity=Severity(value=1, at=lab.result_at),
                    acknowledge=False
                )
