from logbook import Logger

from .. import config
from common.utilities.websocket import websocket_api

logger = Logger(__name__)

websocket_router, notify, notify_property, subscribe = websocket_api(config.redis_connection)


@websocket_router.get('/test_broadcast', tags=["WebSockets"])
async def test_broadcast_key(key, message):
    await notify(key, message)

    return {}
