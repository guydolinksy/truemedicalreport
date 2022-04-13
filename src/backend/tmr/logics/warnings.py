import asyncio
import json
from asyncio import CancelledError

import logbook
from typing import Callable, Coroutine, List

import fastapi
import requests
import websockets
from tmr_common.data_models.patient import Patient

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
async def patient_id_handler(patient_id):
    logger.debug('ID TRIGGER: {}', patient_id)

    await notify(f"/api/patients/id/{patient_id}", {'a': 1})

    # TODO: should trigger notifications only if a notification was added.
    patient = Patient(**requests.get(f"http://medical-dal/medical-dal/patient/id/{patient_id}").json())
    await trigger_notification(patient.wing, patient.oid)


@subscribe(key="patient_bed")
async def patient_bed_handler(patient_bed):
    logger.debug('BED TRIGGER: {}', patient_bed)

    await notify(f"/api/patients/bed/{patient_bed}", {'b': 1})
    # TODO: should trigger notifications only if a notification was added.
    patient = Patient(**requests.get(f"http://medical-dal/medical-dal/patient/bed/{patient_bed}").json())
    await trigger_notification(patient.wing, patient.oid)


@subscribe(key="patient_info")
async def patient_info_handler(patient_id):
    logger.debug('INFO TRIGGER: {}', patient_id)

    await notify(f"/api/patients/id/{patient_id}/info")

    # TODO: should trigger notifications only if a notification was added.
    patient = Patient(**requests.get(f"http://medical-dal/medical-dal/patient/id/{patient_id}").json())
    await trigger_notification(patient.wing, patient.oid)


async def trigger_notification(wing, patient):
    await notify(f"/api/wings/{wing}/notifications", {'openKeys': [patient]})
