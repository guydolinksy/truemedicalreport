import asyncio

from broadcaster import Broadcast
from fastapi import APIRouter
from starlette.websockets import WebSocket


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
            broadcast_messages = aiter(subscriber)
            websocket_messages = aiter(websocket.iter_json())
            read_broadcast, read_websocket, event = None, None, None
            while broadcast_messages and websocket_messages:
                if event:
                    event, _ = None, await websocket.send_json(event.message)
                    continue
                if not read_broadcast:
                    read_broadcast = asyncio.create_task(anext(broadcast_messages))
                if not read_websocket:
                    read_websocket = asyncio.create_task(anext(websocket_messages))
                done, pending = await asyncio.wait([read_broadcast, read_websocket],
                                                   return_when=asyncio.FIRST_COMPLETED)
                if read_websocket in done:
                    try:
                        read_websocket, _ = None, read_websocket.result()
                    except StopAsyncIteration:
                        websocket_messages = None
                if read_broadcast in done:
                    try:
                        read_broadcast, event = None, read_broadcast.result()
                    except StopAsyncIteration:
                        broadcast_messages = None

    async def notify_(key, value=None):
        await broadcast.publish(channel=key, message=value)

    return router_, notify_
