import logbook
import requests
from fastapi import APIRouter, Body

from tmr.logics.utils import prepare_update_object
from tmr_common.data_models.patient import Patient, PatientInfo
from tmr_common.utilities.exceptions import PatientNotFound
from .. import config

patient_router = APIRouter()

logger = logbook.Logger(__name__)


@patient_router.get("/{patient}")
def get_patient_by_id(patient: str) -> dict:
    res = requests.get(f"{config.dal_url}/patients/{patient}")
    if not res.ok:
        raise PatientNotFound()
    return Patient(**res.json()).dict()


@patient_router.get("/{patient}/info")
def get_patient_info_by_id(patient: str) -> dict:
    res = requests.get(f"{config.dal_url}/patients/{patient}/info")
    if not res.ok:
        raise PatientNotFound()
    return PatientInfo(**res.json()).dict()


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"{config.dal_url}/patients/{patient}", json=dict(**update_object)).json()


@patient_router.post("/{patient}/info")
async def update_patient_info_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"{config.dal_url}/patients/{patient}", json=dict(**update_object)).json()
