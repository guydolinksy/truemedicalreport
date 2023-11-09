from typing import Optional, List, Any, Dict, Union

from .admission import Admission
from .awaiting import Awaiting
from .base import AtomicUpdate, Watcher, Diffable
from .discussion import Discussion
from .ecg_record import ECGRecord
from .esi_score import ESIScore
from .image import Image
from .intake import Intake
from .labs import LabCategory
from .mci import MCIBooleanValue, MCIStringValue, MCIResult, MCI
from .measures import Measures, FullMeasures
from .notification import Notification
from .person import Person
from .protocol import Protocol
from .referrals import Referral
from .severity import Severity
from .status import Status
from .treatment import Treatment
from .warnings import PatientWarning
from .watch import WatchKey
from ..utilities.exceptions import PatientNotFoundException


class ExternalData(Diffable):
    external_id: str
    info: Person
    esi: Optional[ESIScore] = None
    admission: Admission
    intake: Intake = Intake()
    discussion: Discussion = Discussion()
    treatment: Treatment = Treatment()
    lab_link: Optional[str] = None
    medical_summary_link: Optional[str] = None
    ecg_records: List[ECGRecord] = []


class Patient(AtomicUpdate, ExternalData):
    collection = 'patients'
    not_found_exception = PatientNotFoundException

    watcher = Watcher()
    status: Status = Status.unassigned
    severity: Optional[Severity] = None
    awaiting: Dict[str, Dict[str, Awaiting]] = {}
    flagged: bool = False
    warnings: Dict[str, PatientWarning] = {}
    measures: Measures = Measures()
    protocol: Protocol = Protocol()
    notifications: Dict[str, Notification] = {}
    referrals: Dict[str, Referral] = {}
    source_identity: Optional[str] = None
    watching: Dict[str, Optional[WatchKey]] = {}

    full_measures: FullMeasures = FullMeasures()
    imaging: Dict[str, Image] = {}
    labs: Dict[str, LabCategory] = {}
    visits: List[Any] = []
    mci: MCI = MCI()
    mci_results: List[MCIResult] = []
    comment: Optional[str] = None

    async def awaiting_intake(self):
        return not any(self.measures.model_dump().values()) and not self.intake.complaint
