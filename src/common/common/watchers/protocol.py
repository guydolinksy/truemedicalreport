from typing import Tuple

from common.data_models.base import Mode, AtomicUpdate
from common.data_models.image import Image
from common.data_models.labs import Laboratory
from common.data_models.measures import Value
from common.data_models.patient import Patient
from common.data_models.protocol import Protocol
from common.data_models.referrals import Referral


@Patient.watcher.callback('intake', 'complaint', mask=Mode.mask_new)
async def handle_complaint_change(new: Patient, new_value: str):
    protocol_config = await AtomicUpdate.get_connection().get_protocol_config()
    new.protocol = Protocol(active=new_value in protocol_config, items=protocol_config.get(new_value, []))


@Patient.watcher.callback('measures', '.*', mask=Mode.mask_new)
async def handle_measures_change(new: 'Patient', path: Tuple[str], new_value: Value):
    await new.protocol.match_protocol(key=f'measure-{path[-1]}', value=new_value.value, at=new_value.at)


@Patient.watcher.callback('imaging', '.*', mask=Mode.mask_new)
async def handle_imaging_change_protocol(new: 'Patient', new_value: Image):
    await new.protocol.match_protocol(
        key=f'imaging-{new_value.title}',
        value=new_value.status_text,
        at=new_value.updated_at
    )


@Patient.watcher.callback('labs', '.*', 'results', '.*', mask=Mode.mask_new)
async def handle_labs_change_protocol(new: 'Patient', new_value: Laboratory):
    await new.protocol.match_protocol(
        key=f'lab-{new_value.test_type_id}',
        value=f'{new_value.result} {new_value.units}' if new_value.result_at else 'הוזמן',
        at=new_value.result_at if new_value.result_at else new_value.ordered_at
    )


@Patient.watcher.callback('referrals', '.*', mask=Mode.mask_new)
async def handle_referrals_change_protocol(new: 'Patient', new_value: Referral):
    await new.protocol.match_protocol(
        key=f'referral-{new_value.to}',
        value=f'הפנייה נסגרה' if new_value.completed_at else 'הפנייה פתוחה',
        at=new_value.completed_at if new_value.completed_at else new_value.at
    )
