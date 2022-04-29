import datetime
from typing import Optional, List

from pydantic import BaseModel

from .imaging import Imaging
from .measures import Measures
from .notification import Notification, NotificationLevel
from .severity import Severity
from .esi_score import ESIScore


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]

    class Config:
        orm_mode = True


class Patient(BaseModel):
    oid: Optional[str]

    # Chameleon fields
    chameleon_id: Optional[str]
    id_: Optional[str]
    esi: Optional[ESIScore]
    name: Optional[str]
    arrival: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    birthdate: Optional[str]
    complaint: Optional[str]
    admission: Optional[Admission]
    measures: Optional[Measures]
    imaging: Optional[List[Imaging]] = []
    notifications: Optional[List[Notification]] = []
    messages: Optional[List[dict]]

    # Internal fields
    awaiting: Optional[str]
    severity: Optional[Severity]
    flagged: Optional[bool]
    warnings: Optional[List[dict]]

    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(Patient, self).__init__(**kwargs)

    def chameleon_dict(self):
        return {
            "chameleon_id": self.chameleon_id,
            "id_": self.id_,
            "name": self.name,
            "arrival": self.arrival,
            "age": self.age,
            "gender": 'male' if self.gender == 'M' else 'female',
            "birthdate": self.birthdate,
            "complaint": self.complaint,
            "admission": self.admission.dict(),
            "esi": self.esi.dict(),
            "imaging": self.imaging,
            "notifications": self.notifications
        }

    def internal_dict(self):
        return {
            "severity": self.severity.dict(),
            "awaiting": self.awaiting,
        }


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
