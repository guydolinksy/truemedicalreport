from common.data_models.base import Mode
from common.data_models.labs import LabCategory
from common.data_models.patient import Patient


@Patient.watcher.callback('labs', '.*', mask=Mode.mask_new)
async def handle_labs_change_warnings(new: Patient, new_value: LabCategory):
    new.warnings.update(new_value.get_updated_warnings(
        {key: warning for key, warning in new.warnings.items() if key.startswith('lab#')}
    ))
