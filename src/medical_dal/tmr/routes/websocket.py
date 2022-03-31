from broadcaster import Broadcast
from fastapi import WebSocket, APIRouter
from logbook import Logger

logger = Logger(__name__)


def websocket_api(broadcast_backing, ws_uri='/ws'):
    router_ = APIRouter()
    broadcast = Broadcast(broadcast_backing)

    @router_.on_event('startup')
    async def on_startup():
        await broadcast.connect()

    @router_.on_event('shutdown')
    async def on_shutdown():
        await broadcast.disconnect()

    @router_.websocket(ws_uri)
    async def websocket_endpoint(websocket: WebSocket, key):
        await websocket.accept()

        async with broadcast.subscribe(channel=key) as subscriber:
            async for event in subscriber:
                await websocket.send_json(event.message)

    async def notify_(key, value):
        await broadcast.publish(channel=key, message=value)

    return router_, notify_


websocket_router, notify = websocket_api("redis://broadcast-redis:6379/1")


@websocket_router.get('/test_broadcast')
async def test_broadcast_key(key, message):
    await notify(key, message)

    return {}
