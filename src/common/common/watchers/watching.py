from typing import Tuple

import logbook

from common.data_models.awaiting import AwaitingTypes, Awaiting
from common.data_models.base import Mode, AtomicUpdate
from common.data_models.image import Image
from common.data_models.labs import Laboratory, LabCategory
from common.data_models.measures import Value
from common.data_models.patient import Patient
from common.data_models.protocol import Protocol
from common.data_models.referrals import Referral
from common.data_models.watch import WatchKey

logger = logbook.Logger(__name__)


@Patient.watcher.callback('measures', '.*', mask=Mode.mask_new)
async def handle_measures_change_watching(new: 'Patient', path: Tuple[str], new_value: Value):
    key = f'measure#{path[-1]}'
    if (watch := new.watching.get(key)) and watch.watched and (not watch.update_at or new_value.at_ > watch.update_at_):
        new.watching[key] = WatchKey(
            triggered=True,
            update_at=new_value.at,
            message=f'עדכון {path[-1]} -> {new_value.value}',
            watched=False
        )


@Patient.watcher.callback('labs', '.*', mask=Mode.mask_new)
async def handle_labs_change_watching(new: Patient, new_value: LabCategory):
    for key, result in new_value.results.items():
        key = f'lab#{key}'
        if result.range == 'LL' or result.range == 'HH':
            if not (watch := new.watching.get(key)) or not watch.update_at or result.result_at_ > watch.update_at_:
                new.watching[key] = WatchKey(
                    triggered=True,
                    update_at=result.result_at,
                    message=f'ערך פאניקה ({result.test_type_name}) -> {result.result} {result.units}',
                    watched=False
                )
            elif result.result_at_ == watch.update_at_ and not result.panic:
                new.watching[key].triggered = False


@Patient.watcher.callback('awaiting', AwaitingTypes.doctor)
async def handle_awaiting_change_watching(new: Patient):
    for key, awaiting in new.awaiting.get(AwaitingTypes.doctor, {}).items():
        if key != 'exam':
            new.watching[f'awaiting#{key}'] = WatchKey(
                triggered=not awaiting.completed_at,
                update_at=awaiting.since,
                message=f'ממתין.ה ל{awaiting.name}',
                watched=False
            )
    awaiting_keys = set(f'awaiting#{key}' for key in new.awaiting.get(AwaitingTypes.doctor, {}) if key != 'exam')
    for key in set(key for key in new.watching if key.startswith('awaiting#')) - awaiting_keys:
        new.watching.pop(key)
