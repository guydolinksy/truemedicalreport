from fastapi import APIRouter
from logbook import Logger

from .. import config
from common.utilities.pubsub import create_publisher

logger = Logger(__name__)

publish_router = APIRouter()
publish = create_publisher(publish_router, config.redis_connection)


@publish_router.get('/test_broadcast', tags=["pubsub"])
async def test_broadcast_key(key, message):
    await publish(key, message)
    return {}
