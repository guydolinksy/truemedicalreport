from typing import Tuple, Any, Optional

from fastapi import APIRouter
from logbook import Logger

from common import Patient
from common.data_models.admission import Admission
from common.utilities.pubsub import create_publisher
from .. import config

logger = Logger(__name__)

publish_router = APIRouter()
publish = create_publisher(publish_router, config.redis_connection)


@Patient.watcher.notify('admission')
async def notify_admission(oid: str, old_value: Optional[Admission], new_value: Optional[Admission]):
    await publish(f'{Patient.__name__}.admission', dict(
        oid=oid,
        old=old_value.model_dump() if old_value else None,
        new=new_value.model_dump() if new_value else None,
    ))


@Patient.watcher.notify()
async def notify_patient(oid: str, old: Optional[Patient], new: Optional[Patient]):
    await publish(f'{Patient.__name__}', dict(
        oid=oid,
        old=old.model_dump() if old else None,
        new=new.model_dump() if new else None,
    ))


@publish_router.get('/test_broadcast', tags=["pubsub"])
async def test_broadcast_key(key, message):
    await publish(key, message)
    return {}
