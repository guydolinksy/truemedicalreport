from logbook import Logger

from tmr_common.utilities.websocket import websocket_api

logger = Logger(__name__)

websocket_router, notify, notify_property, subscribe = websocket_api("redis://broadcast-redis:6379/1")


@websocket_router.get('/test_broadcast', tags=["WebSockets"])
async def test_broadcast_key(key, message):
    await notify(key, message)

    return {}
