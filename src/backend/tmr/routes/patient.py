from json import loads

import requests
from fastapi import APIRouter, Body

from tmr_common.data_models.patient import Patient
from ..utils import prepare_update_object

patient_router = APIRouter()


@patient_router.get("/{patient}")
def get_patient_by_id(patient: str) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/patients/{patient}").json()
    return loads(Patient(**res).json(models_as_dict=False)) if res else None


@patient_router.get("/{patient}/info")
def get_patient_info_by_id(patient: str) -> dict:
    patient = Patient(**requests.get(f"http://medical-dal/medical-dal/patients/{patient}").json())
    res = loads(patient.json(models_as_dict=False))
    res.pop('measures')
    return res


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"http://medical-dal/medical-dal/patients/{patient}", json=dict(**update_object)).json()


@patient_router.post("/{patient}/info")
async def update_patient_info_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"http://medical-dal/medical-dal/patients/{patient}", json=dict(**update_object)).json()
