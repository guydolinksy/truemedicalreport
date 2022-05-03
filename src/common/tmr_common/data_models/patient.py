import datetime
from typing import Optional, List, Any

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


class Warning(BaseModel):
    class Config:
        orm_mode = True


class ExternalPatient(BaseModel):
    external_id: str
    id_: Optional[str]
    esi: Optional[ESIScore]
    name: Optional[str]
    arrival: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    birthdate: Optional[str]
    complaint: Optional[str]
    admission: Optional[Admission]
    measures: Measures

    def __init__(self, **kwargs):
        if 'gender' in kwargs and kwargs['gender'] in ['M', 'F']:
            kwargs['gender'] = 'male' if kwargs['gender'] == 'M' else 'female'
        super(ExternalPatient, self).__init__(**kwargs)


class InternalPatient(BaseModel):
    awaiting: Optional[str]
    severity: Severity
    flagged: bool
    warnings: List[Warning]

    class Config:
        orm_mode = True

    @classmethod
    def from_external_patient(cls, patient: ExternalPatient):
        return cls(severity=Severity(**patient.esi.dict()), awaiting='מחכה לך', flagged=False, warnings=[])


class Patient(BaseModel):
    oid: str
    external_data: ExternalPatient
    internal_data: InternalPatient

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        if 'external_data' not in kwargs:
            kwargs['external_data'] = ExternalPatient(**kwargs)
        if 'internal_data' not in kwargs:
            kwargs['internal_data'] = InternalPatient(**kwargs)
        super(Patient, self).__init__(**kwargs)


class ExtendedPatient(BaseModel):
    imaging: List[Imaging] = []
    full_measures: List[Any] = []
    labs: List[Any] = []
    referrals: List[Any] = []
    notifications: List[Any] = []
    visits: List[Any] = []
    events: List[Any] = []

    class Config:
        orm_mode = True


class PatientInfo(Patient):
    extended_data: ExtendedPatient

    def __init__(self, **kwargs):
        if 'extended_data' not in kwargs:
            kwargs['extended_data'] = ExtendedPatient(**kwargs)
        super(PatientInfo, self).__init__(**kwargs)


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
