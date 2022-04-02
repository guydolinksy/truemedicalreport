import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable, Coroutine

import requests
import websockets

from tmr.routes.websocket import notify
from tmr_common.data_models.patient import Patient

logger = logging.getLogger(__name__)


@dataclass
class WebSocketSubscriber:
    websocket_url: str

    def subscribe(self, key: str):
        def decorator(func: Callable[[str], Coroutine]):
            async def wrapper():
                async with websockets.connect(f"{self.websocket_url}?key={key}") as ws:
                    async for message in ws:
                        await func(message)
            return wrapper
        return decorator


subscriber = WebSocketSubscriber(websocket_url="ws://medical_dal/medical_dal/sync/ws")


@subscriber.subscribe(key="patient")
async def patient_handler(patient_id):

    patient = Patient(**requests.get(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}").json())
    if patient.bed:
        notify(f"/api/patients/bed/{patient.bed}")
    else:
        notify(f"/api/patients/id/{patient_id}")

