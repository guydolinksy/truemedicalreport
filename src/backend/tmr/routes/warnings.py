import json

import logbook
import requests
from fastapi import Body

from tmr_common.data_models.patient import Patient, Admission
from tmr_common.utilities.websocket import websocket_subscriber
from .websocket import notify

logger = logbook.Logger(__name__)

subscriber_router, subscribe = websocket_subscriber(websocket_url="ws://medical-dal/medical-dal/sync/ws")


@subscribe(key=Patient.__name__)
@subscriber_router.post('/patients/{patient}')
async def patient_handler(patient: str):
    await notify(f"/api/patients/{patient}")
    await notify(f"/api/patients/{patient}/info")

    patient = Patient(**requests.get(f"http://medical-dal/medical-dal/patients/{patient}").json())
    await notify(f"/api/departments/{patient.admission.department}")
    await notify(f"/api/departments/{patient.admission.department}/wings/{patient.admission.wing}")


@subscribe(key=Admission.__name__, mapper=lambda m: Admission(**json.loads(m)))
@subscriber_router.post('/admissions')
async def admission_handler(admission: Admission = Body(..., embed=True)):
    await notify(f"/api/departments/{admission.department}")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}/beds/{admission.bed}")


async def trigger_status(patient: Patient, should_open=False):
    if patient.admission:
        await notify(
            f"/api/departments/{patient.admission.department}/wings/{patient.admission.wing}",
            {'openKeys': [patient.oid] if should_open else []})
