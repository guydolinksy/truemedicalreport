import asyncio
import json
import typing
from asyncio import Future, CancelledError
from collections import defaultdict
from typing import List, Dict, Set, Coroutine, Callable, Any

import fastapi
import logbook
import websockets
from broadcaster import Broadcast
from fastapi import APIRouter
from pymongo.errors import DuplicateKeyError
from starlette.websockets import WebSocket, WebSocketDisconnect

from tmr_common.utilities.exceptions import MaxRetriesExceeded
from tmr_common.utilities.json_utils import json_to_dot_notation

logger = logbook.Logger(__name__)

CHANNEL = 'updates'


def websocket_subscriber(websocket_url):
    handlers: List[Coroutine] = []
    router_ = fastapi.APIRouter()
    tasks = []

    def subscribe_(key: str, mapper: Callable[[Any], Any] = json.loads):
        def decorator(func: Callable[[str], Coroutine]):
            async def wrapper():
                try:
                    async for ws in websockets.connect(f"{websocket_url}?key={key}"):
                        async for message in ws:
                            try:
                                await func(mapper(message))
                            except Exception:
                                logger.exception('Error running handler for message: {}', message)
                except CancelledError:
                    pass

            handlers.append(wrapper())
            return func

        return decorator

    @router_.on_event('startup')
    async def on_startup():
        for func in handlers:
            tasks.append(asyncio.create_task(func))

    @router_.on_event('shutdown')
    async def on_shutdown():
        for task in tasks:
            task.cancel()

    return router_, subscribe_


def websocket_api(broadcast_backing, ws_uri='/ws'):
    class Wrapper(object):
        def __init__(self, callback):
            self.callback = callback

        async def send_json(self, data: typing.Any, mode: str = "text") -> None:
            try:
                await self.callback(data)
            except:
                logger.exception('Error running handler for message: {}', data)

    router_ = APIRouter()
    broadcast = Broadcast(broadcast_backing)
    connections: Dict[str, List[WebSocket | Wrapper]] = defaultdict(lambda: [])
    listener: Set[Future] = set()

    def subscribe(key):
        def decorator(func: Callable[[str], Coroutine]):
            connections[key].append(Wrapper(func))
            return func

        return decorator

    async def listen():
        async with broadcast.subscribe(channel=CHANNEL) as subscriber:
            async for event in subscriber:
                key, message = json.loads(event.message)
                living_connections = []
                while connections[key]:
                    websocket = connections[key].pop()
                    await websocket.send_json(message)
                    living_connections.append(websocket)
                connections[key] = living_connections

    @router_.on_event('startup')
    async def on_startup():
        await broadcast.connect()
        listener.add(asyncio.ensure_future(listen()))

    @router_.on_event('shutdown')
    async def on_shutdown():
        await broadcast.disconnect()
        for handler in listener:
            if handler.done():
                handler.result()

    @router_.websocket(ws_uri)
    async def websocket_endpoint(websocket: WebSocket, key):
        await websocket.accept()
        connections[key].append(websocket)
        try:
            while True:
                msg = await websocket.receive_json()
                await websocket.send_json(msg)
        except WebSocketDisconnect:
            connections[key].remove(websocket)

    async def notify_(key, value: Any = ''):
        await broadcast.publish(channel=CHANNEL, message=json.dumps((key, value)))

    async def notify_property_(type_: str, key: str, attr: str, old: str, new: str):
        if key:
            await notify_('.'.join([type_, attr]), dict(key=key, old=old, new=new))

    return router_, notify_, notify_property_, subscribe


def atomic_update(klass, collection, notify, notify_property, max_retries=10):
    async def _atomic_update(query: dict, new: dict) -> bool:
        update = json_to_dot_notation(new)
        old = None
        for i in range(max_retries):
            prv = collection.find_one(query)
            old = json_to_dot_notation(klass(**prv).dict(include=set(new), exclude_unset=True)) if prv else {}

            if all(k in old and update[k] == old[k] for k in update):
                return False
            try:
                update_result = collection.update_one({**query, **old}, {'$set': update}, upsert=True)
                if update_result.modified_count:
                    break
            except DuplicateKeyError:
                pass
        else:
            raise MaxRetriesExceeded(f'{query}: {old} -> {new}')

        oid = str(collection.find_one(query).pop('_id'))
        for k in new:
            if old.get(k) != new.get(k):
                await notify_property(klass.__name__, oid, k, old.get(k), update.get(k))

        return await notify(klass.__name__, oid)

    return _atomic_update
