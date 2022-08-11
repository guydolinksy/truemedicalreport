import datetime
from enum import Enum
from typing import Optional, List, Any, Dict

from pydantic import BaseModel

from .esi_score import ESIScore
from .image import Image
from .measures import Measures, FullMeasures
from .notification import Notification, NotificationLevel
from .severity import Severity
from .labs import LabCategory
from .warnings import PatientWarning
from .treatment import Treatment


class Admission(BaseModel):
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]


class BasicMedical(BaseModel):
    nurse_description: Optional[str]
    nurse_seen_time: Optional[str]
    doctor_seen_time: Optional[str]


class ExternalPatient(BaseModel):
    external_id: Optional[str]
    id_: Optional[str]
    esi: ESIScore = ESIScore()
    name: Optional[str]
    arrival: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    birthdate: Optional[str]
    complaint: Optional[str]
    admission: Admission = Admission()
    discharge_time: Optional[str]
    treatment: Treatment = Treatment()
    basic_medical: BasicMedical = BasicMedical()

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
    severity: Severity =Severity()
    awaiting: Dict[str, Dict[str, Awaiting]] = {}
    flagged: bool
    warnings: Dict[str, PatientWarning] = {}
    measures: Measures = Measures()

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
