import datetime
from enum import Enum
from typing import Optional, List, Any, Dict

from pydantic import BaseModel

from .esi_score import ESIScore
from .image import Image
from .labs import LabCategory
from .measures import Measures, FullMeasures
from .notification import Notification, NotificationLevel
from .severity import Severity


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]


class Warning(BaseModel):
    content: str
    severity: Severity


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

    def __init__(self, **kwargs):
        if 'gender' in kwargs and kwargs['gender'] in ['M', 'F']:
            kwargs['gender'] = 'male' if kwargs['gender'] == 'M' else 'female'
        super(ExternalPatient, self).__init__(**kwargs)


class Icon(Enum):
    pulse = 1
    temperature = 2
    saturation = 3
    blood_pressure = 4
    imaging = 5
    laboratory = 6
    doctor = 7
    nurse = 8
    referral = 9


class Awaiting(BaseModel):
    awaiting: str
    since: str
    limit: int
    completed: bool = False

    class Config:
        orm_mode = True
        use_enum_values = True


class AwaitingTypes(Enum):
    doctor = "doctor"
    nurse = "nurse"
    imaging = "imaging"
    laboratory = "laboratory"
    referral = "referral"


class InternalPatient(BaseModel):
    awaiting: Dict[str, Dict[str, Awaiting]]
    severity: Severity
    flagged: bool
    warnings: List[Warning]
    measures: Measures

    class Config:
        orm_mode = True

    @classmethod
    def from_external_patient(cls, patient: ExternalPatient):
        return cls(
            severity=Severity(**patient.esi.dict()),
            awaiting={
                AwaitingTypes.doctor.value: {
                    'exam': Awaiting(awaiting='בדיקת צוות רפואי', since=patient.arrival, limit=1500)
                },
                AwaitingTypes.nurse.value: {
                    'exam': Awaiting(awaiting='בדיקת צוות סיעודי', since=patient.arrival, limit=1500)
                },
            },
            flagged=False,
            warnings=[],
            measures=Measures(),
        )


class Patient(ExternalPatient, InternalPatient):
    oid: str

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(Patient, self).__init__(**kwargs)


class Event(BaseModel):
    key: str
    content: str
    at: str


class ExtendedPatient(BaseModel):
    full_measures: FullMeasures
    visits: List[Any] = []
    notifications: List[Any] = []
    imaging: List[Image] = []
    labs: List[LabCategory] = []
    referrals: List[Any] = []
    events: List[Event] = []

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
