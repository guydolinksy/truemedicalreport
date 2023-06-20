import datetime
from typing import List, Any, Dict
from typing import Optional

from pydantic import BaseModel

from common.data_models.notification import Notification, NotificationLevel
from common.data_models.patient import Patient


class WingDetails(BaseModel):
    oid: Optional[str]
    name: Optional[str]
    key: Optional[str]
    department: Optional[str]
    columns: Optional[List[dict]]
    rows: Optional[List[dict]]
    beds: Optional[List[List[Optional[str]]]]

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(WingDetails, self).__init__(**kwargs)


class WingFilter(BaseModel):
    key: str
    count: int
    title: str
    icon: str
    duration: Optional[str]
    valid: bool = True
    children: List[Any] = list()

    class Config:
        orm_mode = True


class WingFilters(BaseModel):
    awaiting: List[WingFilter]
    doctors: List[WingFilter]
    treatments: List[WingFilter]
    mapping: Dict[str, List[str]]

    class Config:
        orm_mode = True


class PatientNotifications(BaseModel):
    patient: Patient

    notifications: List[Notification]

    at: Optional[str]
    preview: Optional[str]
    level: NotificationLevel = NotificationLevel.normal

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if 'at' not in kwargs and kwargs['notifications']:
            notifications_: List[Notification] = kwargs['notifications']
            kwargs['at'] = max(notifications_, key=lambda n: datetime.datetime.fromisoformat(n.at)).at
        if 'level' not in kwargs and kwargs['notifications']:
            notifications_: List[Notification] = kwargs['notifications']
            kwargs['level'] = NotificationLevel(min(notifications_, key=lambda n: n.level).level)
        if 'preview' not in kwargs and kwargs['notifications']:
            notifications_: List[Notification] = kwargs['notifications']
            kwargs['preview'] = ', '.join([n.message for n in notifications_])
        super(PatientNotifications, self).__init__(**kwargs)


class Wing(BaseModel):
    department_patients: List[Patient]
    patients: List[Patient]
    details: WingDetails
    filters: WingFilters
    notifications: List[PatientNotifications]

    class Config:
        orm_mode = True


class WingSummary(BaseModel):
    details: WingDetails
    filters: WingFilters
    count: int

    class Config:
        orm_mode = True
