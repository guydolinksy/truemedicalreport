from typing import Optional, List, Any, Dict

from pydantic import BaseModel

from .admission import Admission
from .awaiting import Awaiting, AwaitingTypes
from .ecg_record import ECGRecord
from .discussion import Discussion
from .esi_score import ESIScore
from .event import Event
from .image import Image
from .intake import Intake
from .labs import LabCategory
from .measures import Measures, FullMeasures
from .notification import Notification
from .protocol import Protocol
from .referrals import Referral
from .severity import Severity
from .status import Status
from .treatment import Treatment
from .warnings import PatientWarning
from .watch import WatchKey


class Person(BaseModel):
    id_: Optional[str]
    name: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    birthdate: Optional[str]
    phone: Optional[str]


class ExternalPatient(BaseModel):
    external_id: Optional[str]
    info: Person = Person()
    esi: ESIScore = ESIScore()
    admission: Admission = Admission()
    intake: Intake = Intake()
    discussion: Discussion = Discussion()
    treatment: Treatment = Treatment()
    lab_link: Optional[str]
    medical_summary_link: Optional[str]
    ecg_records: List[ECGRecord] = []


class InternalPatient(BaseModel):
    status: Status = Status.unassigned.value
    severity: Severity = Severity()
    awaiting: Dict[str, Dict[str, Awaiting]] = {}
    flagged: Optional[bool]
    warnings: Dict[str, PatientWarning] = {}
    measures: Measures = Measures()
    protocol: Protocol = Protocol()
    notifications: List[Notification] = []
    referrals: List[Referral] = []
    watching: Dict[str, Optional[WatchKey]] = {}

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def from_external_patient(cls, patient: ExternalPatient):
        return cls(
            status=Status.unassigned.value,
            severity=Severity(**patient.esi.dict()),
            awaiting={
                AwaitingTypes.doctor.value: {
                    'exam': Awaiting(subtype='exam', name='בדיקת צוות רפואי', since=patient.admission.arrival or "",
                                     status='לא בוצעה', limit=1500)
                },
                AwaitingTypes.nurse.value: {
                    'exam': Awaiting(subtype='exam', name='בדיקת צוות סיעודי', since=patient.admission.arrival or "",
                                     status='לא בוצעה', limit=1500)
                },
            },
            flagged=False,
            warnings={},
            measures=Measures(),
        )


class Patient(ExternalPatient, InternalPatient):
    oid: Optional[str]

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(Patient, self).__init__(**kwargs)


class PatientInfoPluginRender(BaseModel):
    key: str
    title: str
    url: str


class PatientInfoPluginConfig(BaseModel):
    key: str
    title: str
    url: str
    api_version: str

    def render(self, **kwargs):
        return PatientInfoPluginRender(
            key=self.key,
            title=self.title.format(**kwargs),
            url=self.url.format(**kwargs),
        )


class AggregatePatient(BaseModel):
    full_measures: FullMeasures
    visits: List[Any] = []
    imaging: List[Image] = []
    labs: List[LabCategory] = []
    events: List[Event] = []

    class Config:
        orm_mode = True


class PatientInfo(Patient, AggregatePatient):
    pass


class PanelPatient(PatientInfo):
    plugins: List[PatientInfoPluginRender] = []
