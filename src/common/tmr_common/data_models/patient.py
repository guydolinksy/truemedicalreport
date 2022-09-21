from typing import Optional, List, Any, Dict

from pydantic import BaseModel

from tmr_common.data_models.esi_score import ESIScore
from .admission import Admission
from .awaiting import Awaiting, AwaitingTypes
from .event import Event
from .image import Image
from tmr_common.data_models.measures import Measures, FullMeasures
from .intake import Intake
from .severity import Severity
from .labs import LabCategory
from tmr_common.data_models.warnings import PatientWarning
from .treatment import Treatment


class Person(BaseModel):
    id_: Optional[str]
    name: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    birthdate: Optional[str]


class ExternalPatient(BaseModel):
    external_id: Optional[str]
    info: Person = Person()
    esi: ESIScore = ESIScore()
    admission: Admission = Admission()
    intake: Intake = Intake()
    treatment: Treatment = Treatment()


class InternalPatient(BaseModel):
    severity: Severity = Severity()
    awaiting: Dict[str, Dict[str, Awaiting]] = {}
    flagged: Optional[bool]
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
                    'exam': Awaiting(subtype='exam', name='בדיקת צוות רפואי', since=patient.admission.arrival, limit=1500)
                },
                AwaitingTypes.nurse.value: {
                    'exam': Awaiting(subtype='exam', name='בדיקת צוות סיעודי', since=patient.admission.arrival, limit=1500)
                },
            },
            flagged=False,
            warnings=[],
            measures=Measures(),
        )


class Patient(ExternalPatient, InternalPatient):
    oid: Optional[str]

    def __init__(self, **kwargs):
        if '_id' in kwargs:
            kwargs['oid'] = str(kwargs.pop('_id'))
        super(Patient, self).__init__(**kwargs)


class AggregatePatient(BaseModel):
    full_measures: FullMeasures
    visits: List[Any] = []
    notifications: List[Any] = []
    imaging: List[Image] = []
    labs: List[LabCategory] = []
    referrals: List[Any] = []
    events: List[Event] = []

    class Config:
        orm_mode = True


class PatientInfo(Patient, AggregatePatient):
    pass


