import logbook

from common.data_models.base import Mode
from common.data_models.patient import Patient
from common.data_models.status import Status
from common.data_models.treatment import Treatment

logger = logbook.Logger(__name__)
@Patient.watcher.callback('treatment', mask=Mode.mask_new)
async def handle_treatment_change_status(path:str, new: Patient, new_value: Treatment):
    if new_value.destination:
        new.status = Status.decided
    elif new_value.doctors:
        new.status = Status.undecided
    else:
        new.status = Status.unassigned

