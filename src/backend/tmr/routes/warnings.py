import json

import logbook
import requests
from fastapi import Body

from tmr_common.data_models.admission import Admission
from tmr_common.data_models.patient import Patient
from tmr_common.utilities.websocket import websocket_subscriber
from .websocket import notify
from .. import config

logger = logbook.Logger(__name__)

subscriber_router, subscribe = websocket_subscriber(websocket_url=config.ws_url)
# TODO: sync error - backend does not reconnect if dal was restarted and web socket was closed.

@subscribe(key=Patient.__name__)
@subscriber_router.post('/patients/{patient}')
async def patient_handler(patient: str):
    await notify(f"/api/patients/{patient}")
    await notify(f"/api/patients/{patient}/info")

    patient = Patient(**requests.get(f"{config.dal_url}/patients/{patient}").json())
    await notify(f"/api/departments/{patient.admission.department}")
    await notify(f"/api/departments/{patient.admission.department}/wings/{patient.admission.wing}")


@subscribe(key=f'{Patient.__name__}.admission', mapper=lambda m: Admission(**json.loads(m)))
@subscriber_router.post('/admissions')
async def admission_handler(admission: Admission = Body(..., embed=True)):
    logger.debug('UPDATE ADMISSION {}', admission)
    await notify(f"/api/departments/{admission.department}")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}")
    await notify(f"/api/departments/{admission.department}/wings/{admission.wing}/beds/{admission.bed}")


async def trigger_status(patient: Patient, should_open=False):
    if patient.admission:
        await notify(
            f"/api/departments/{patient.admission.department}/wings/{patient.admission.wing}",
            {'openKeys': [patient.oid] if should_open else []})
