from logbook import Logger

from tmr_common.utilities.websocket import websocket_api
from .. import config

logger = Logger(__name__)

websocket_router, notify, notify_property, subscribe = websocket_api(config.redis_connection)


@websocket_router.get('/test_broadcast')
async def test_broadcast_key(key, message):
    await notify(key, message)

    return {}
