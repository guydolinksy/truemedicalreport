import asyncio
import json
from asyncio import CancelledError

import logbook
from typing import Callable, Coroutine, List

import fastapi
import websockets

from tmr.routes.websocket import notify

logger = logbook.Logger(__name__)


def websocket_subscriber(websocket_url):
    handlers: List[Coroutine] = []
    router_ = fastapi.APIRouter()
    tasks = []

    def subscribe_(key: str):
        def decorator(func: Callable[[str], Coroutine]):
            async def wrapper():
                try:
                    async for ws in websockets.connect(f"{websocket_url}?key={key}"):
                        async for message in ws:
                            await func(json.loads(message))
                except CancelledError:
                    pass

            handlers.append(wrapper())
            return wrapper

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


subscriber_router, subscribe = websocket_subscriber(websocket_url="ws://medical-dal/medical-dal/sync/ws")


@subscribe(key="patient_id")
async def patient_handler(patient_id):
    await notify(f"/api/patients/id/{patient_id}")


@subscribe(key="patient_bed")
async def patient_handler(patient_bed):
    await notify(f"/api/patients/bed/{patient_bed}")
