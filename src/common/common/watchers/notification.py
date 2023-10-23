from common.data_models.base import Mode
from common.data_models.image import Image
from common.data_models.labs import LabCategory
from common.data_models.patient import Patient
from common.data_models.referrals import Referral


@Patient.watcher.callback('imaging', '.*', mask=Mode.mask_new)
async def handle_imaging_change_notification(new: Patient, new_value: Image):
    new.notifications.update(new_value.to_notifications())


@Patient.watcher.callback('imaging', '.*', mask=Mode.mask_all, mode=Mode.deleted)
async def handle_imaging_pop_notification(new: Patient, old_value: Image):
    if new:
        for static_id in old_value.to_notifications():
            new.notifications.pop(static_id, None)


@Patient.watcher.callback('labs', '.*', mask=Mode.mask_new)
async def handle_labs_change_notification(new: Patient, new_value: LabCategory):
    new.notifications.update(new_value.to_notifications())

    # TODO: add after db callbacks and listners for FE:
    #  await publish("notification", patient.oid)


@Patient.watcher.callback('referrals', '.*', mask=Mode.mask_new)
async def handle_referrals_change_notification(new: Patient, new_value: Referral):
    new.notifications.update(new_value.to_notifications())
