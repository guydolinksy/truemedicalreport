import datetime
from typing import Optional, List
from pydantic import BaseModel

from .patient import Patient, NotificationLevel, Notification


class PatientNotifications(BaseModel):
    patient: Patient

    notifications: Optional[List[Notification]]

    at: Optional[str]
    level: Optional[NotificationLevel]

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        if 'notifications' not in kwargs:
            patient_: Patient = kwargs['patient']
            kwargs['notifications'] = sorted(patient_.notifications,
                                             key=lambda n: datetime.datetime.fromisoformat(n.at))
        if 'at' not in kwargs and kwargs['notifications']:
            notifications_: List[Notification] = kwargs['notifications']
            kwargs['at'] = max(notifications_, key=lambda n: datetime.datetime.fromisoformat(n.at)).at
        if 'level' not in kwargs and kwargs['notifications']:
            notifications_: List[Notification] = kwargs['notifications']
            kwargs['level'] = min(notifications_, key=lambda n: n.level.value).level
        super(PatientNotifications, self).__init__(**kwargs)
