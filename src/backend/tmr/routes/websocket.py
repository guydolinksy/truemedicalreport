import asyncio
from asyncio import Condition

from broadcaster import Broadcast
from fastapi import WebSocket, APIRouter
from logbook import Logger
from starlette.websockets import WebSocketState

logger = Logger(__name__)


class EventManager(object):
    def __init__(self):
        self.events = {}
        self.cancelled = False

    async def wait(self, key):
        if not self.cancelled:
            event = self.events.setdefault(key, Condition())
            async with event:
                return await event.wait()

    async def notify(self, key):
        event = self.events.setdefault(key, Condition())
        async with event:
            event.notify_all()

    async def close(self):
        old_events, self.events, self.cancelled = self.events.values(), {}, True
        for event in old_events:
            async with event:
                event.notify_all()


def websocket_api(broadcast_backing, ws_uri='/ws', channel='sync'):
    events = EventManager()
    router_ = APIRouter()
    broadcast = Broadcast(broadcast_backing)

    @router_.on_event('startup')
    async def on_startup():
        await broadcast.connect()

        async def listen():
            async with broadcast.subscribe(channel=channel) as subscriber:
                async for event in subscriber:
                    await events.notify(event.message)

        asyncio.create_task(listen())

    @router_.on_event('shutdown')
    async def on_shutdown():
        await events.close()
        await broadcast.disconnect()

    @router_.websocket(ws_uri)
    async def websocket_endpoint(websocket: WebSocket, key):
        await websocket.accept()

        wait = None
        receive = None
        while websocket.client_state != WebSocketState.DISCONNECTED:
            if not wait:
                wait = asyncio.create_task(events.wait(key))
            if not receive:
                receive = asyncio.create_task(websocket.receive())

            done, pending = await asyncio.wait([wait, receive], return_when=asyncio.FIRST_COMPLETED)

            if receive in done:
                receive.result()
                receive = None
            if wait in done:
                await websocket.send_json(wait.result())
                wait = None

    async def notify_(key):
        await broadcast.publish(channel=channel, message=key)

    return router_, notify_


websocket_router, notify = websocket_api("redis://broadcast-redis:6379/0")


@websocket_router.get('/test_broadcast')
async def test_broadcast_key(key):
    await notify(key)

    return {}
