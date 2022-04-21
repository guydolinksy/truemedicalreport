import asyncio
import json
from asyncio import CancelledError
from typing import Callable, Coroutine, List, Any

import fastapi
import logbook
import requests
import websockets
from fastapi import Body

from tmr_common.data_models.patient import Patient, Admission
from ..routes.websocket import notify

logger = logbook.Logger(__name__)


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


subscriber_router, subscribe = websocket_subscriber(websocket_url="ws://medical-dal/medical-dal/sync/ws")


@subscribe(key="patient")
@subscriber_router.post('/patients/{patient}')
async def patient_handler(patient: str):
    await notify(f"/api/patients/{patient}")
    await notify(f"/api/patients/{patient}/info")

    # TODO: should trigger notifications only if a notification was added.
    patient = Patient(**requests.get(f"http://medical-dal/medical-dal/patients/{patient}").json())
    await trigger_notification(patient)


@subscribe(key="admission", mapper=lambda message: Admission(**json.loads(message)))
@subscriber_router.post('/admissions')
async def admission_handler(admission: Admission = Body(..., embed=True)):
    await notify(f"/api/departments/{admission.department}")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}/notifications")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}/beds/{admission.bed}")


async def trigger_notification(patient: Patient):
    if patient.admission:
        await notify(f"/api/departments/{patient.admission.department}/wings/{patient.admission.wing}/notifications",
                     {'openKeys': [patient.oid]})
