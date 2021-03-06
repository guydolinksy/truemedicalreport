import logbook
import requests
from fastapi import APIRouter, Body
from werkzeug.exceptions import NotFound

from tmr_common.data_models.patient import Patient, PatientInfo
from ..utils import prepare_update_object

patient_router = APIRouter()

logger = logbook.Logger(__name__)


@patient_router.get("/{patient}")
def get_patient_by_id(patient: str) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/patients/{patient}").json()
    if not res:
        raise NotFound()
    return Patient(**res).dict()


@patient_router.get("/{patient}/info")
def get_patient_info_by_id(patient: str) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/patients/{patient}/info").json()
    if not res:
        raise NotFound()
    return PatientInfo(**res).dict()


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"http://medical-dal/medical-dal/patients/{patient}", json=dict(**update_object)).json()


@patient_router.post("/{patient}/info")
async def update_patient_info_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"http://medical-dal/medical-dal/patients/{patient}", json=dict(**update_object)).json()
