import datetime
from typing import Optional, List, Any

from pydantic import BaseModel

from .imaging import Imaging
from .measures import Measures, Pressure, Systolic, FullMeasures
from .notification import Notification, NotificationLevel
from .severity import Severity
from .esi_score import ESIScore


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]


class Warning(BaseModel):
    pass


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
    measures: Optional[Measures]

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


class Patient(ExternalPatient, InternalPatient):
    oid: str

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(Patient, self).__init__(**kwargs)


class ExtendedPatient(BaseModel):
    full_measures: FullMeasures
    imaging: List[Imaging] = []
    labs: List[Any] = []
    referrals: List[Any] = []
    notifications: List[Any] = []
    visits: List[Any] = []
    events: List[Any] = []

    class Config:
        orm_mode = True


class PatientInfo(Patient, ExtendedPatient):
    pass


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
