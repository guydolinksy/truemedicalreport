import logbook

from common.data_models.awaiting import AwaitingTypes, Awaiting
from common.data_models.base import Mode
from common.data_models.image import Image
from common.data_models.labs import LabCategory, LabStatus
from common.data_models.medication import Medication
from common.data_models.patient import Patient
from common.data_models.referrals import Referral
from common.data_models.intake import Intake

logger = logbook.Logger(__name__)


@Patient.watcher.callback('intake', 'doctor_seen_time', mask=Mode.mask_new)
async def handle_intake_doctor_seen_time_change_awaiting(new: Patient, new_value: str):
    new.awaiting.get(AwaitingTypes.doctor, {}).__setitem__('exam', Awaiting(
        subtype='exam',
        name='בדיקת צוות רפואי',
        since=new.admission.arrival or "",
        status='הושלמה',
        limit=1500,
        completed_at=new_value
    ))


@Patient.watcher.callback('intake', mask=Mode.mask_new)
async def handle_intake_nurse_description_change_awaiting(new: Patient, new_value: Intake):
    if new_value.nurse_seen_time and new_value.nurse_description:
        new.awaiting.setdefault(AwaitingTypes.nurse, {}).__setitem__('exam', Awaiting(
            subtype='exam',
            name='בדיקת צוות סיעודי',
            since=new.admission.arrival or "",
            status='הושלמה',
            limit=1500,
            completed_at=new_value.nurse_seen_time
        ))


@Patient.watcher.callback('imaging', '.*', mask=Mode.mask_new)
async def handle_imaging_change_awaiting(new: Patient, new_value: Image):
    new.awaiting.setdefault(AwaitingTypes.imaging, {}).__setitem__(new_value.external_id, Awaiting(
        subtype=new_value.title,
        name=new_value.title,
        since=new_value.ordered_at,
        completed_at=new_value.updated_at if new_value._is_completed() else None,
        status=new_value.status_text,
        limit=3600,
    ))


@Patient.watcher.callback('imaging', '.*', mask=Mode.mask_all, mode=Mode.deleted)
async def handle_imaging_pop_awaiting(new: Patient, old_value: Image):
    if new:
        new.awaiting.get(AwaitingTypes.imaging, {}).pop(old_value.external_id, None)


@Patient.watcher.callback('labs', '.*', mask=Mode.mask_new)
async def handle_labs_change_awaiting(new: Patient, new_value: LabCategory):
    new.awaiting.setdefault(AwaitingTypes.laboratory, {}).__setitem__(new_value.external_id, Awaiting(
        subtype=new_value.category,
        name=new_value.category_display_name,
        since=new_value.ordered_at,
        completed_at=new_value.ordered_at if new_value.status == LabStatus.analyzed else None,
        status={
            LabStatus.ordered: 'הוזמן',
            LabStatus.collected: 'שויכו דגימות',
            LabStatus.in_progress: 'בעבודה',
            LabStatus.analyzed: 'תוצאות',
        }.get(new_value.status, '?'),
        limit=3600,
    ))


@Patient.watcher.callback('labs', '.*', mask=Mode.mask_all, mode=Mode.deleted)
async def handle_labs_pop_awaiting(new: Patient, old_value: LabCategory):
    if new:
        new.awaiting.get(AwaitingTypes.laboratory, {}).pop(old_value.external_id, None)


@Patient.watcher.callback('referrals', '.*', mask=Mode.mask_new)
async def handle_referrals_change_awaiting(new: Patient, new_value: Referral):
    new.awaiting.setdefault(AwaitingTypes.referral, {}).__setitem__(new_value.external_id, Awaiting(
        subtype=new_value.to,
        name=new_value.to,
        since=new_value.at,
        completed_at=new_value.completed_at,
        status='סגורה' if new_value.completed_at else 'פתוחה',
        limit=3600,
    ))


@Patient.watcher.callback('treatment', 'medications', '.*', mask=Mode.mask_new)
async def handle_treatment_medications_change_awaiting(new: Patient, new_value: Medication):
    new.awaiting.setdefault(AwaitingTypes.nurse, {}).__setitem__(new_value.external_id, Awaiting(
        since=new_value.since,
        subtype="הוראות פעילות",
        name=f"{new_value.label}-{new_value.dosage}",
        completed_at=new_value.given,
        status='ממתין' if new_value.given else 'ניתן',
        limit=1500,
    ))


@Patient.watcher.callback('awaiting', mask=Mode.mask_new)
@Patient.watcher.callback('treatment', 'destination', mask=Mode.mask_new)
async def handle_awaiting_change_awaiting(new: Patient):
    data = [awaiting.completed_at for type_ in [
        AwaitingTypes.imaging, AwaitingTypes.laboratory, AwaitingTypes.referral
    ] for key, awaiting in new.awaiting.get(type_, {}).items()]

    if data and all(data):
        new.awaiting.setdefault(AwaitingTypes.doctor, {}).__setitem__('decision', Awaiting(
            since=max(data),
            subtype="החלטה",
            name="החלטה",
            completed_at=max(data) if new.treatment.destination else None,
            status='התקבלה' if new.treatment.destination else 'ממתין',
            limit=1500,
        ))
    elif data and not all(data):
        new.awaiting.get(AwaitingTypes.doctor, {}).pop('decision', None)
