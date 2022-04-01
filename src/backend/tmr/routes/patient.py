from fastapi import APIRouter, Body
import requests
from tmr_common.data_models.patient import Patient
from tmr_common.data_models.measures.measures import Measures
from json import loads

from .websocket import notify

from ..utils import prepare_update_object

patient_router = APIRouter()


@patient_router.get("/bed/{bed}")
def get_patient_info_by_bed(bed: str) -> dict:
    patient = Patient(**requests.get(f"http://medical_dal:8050/medical_dal/patient/bed/{bed}").json())
    return loads(patient.json(models_as_dict=False))


@patient_router.get("/id/{patient_id}")
def get_patient_info_by_id(patient_id: str) -> dict:
    patient = Patient(**requests.get(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}").json())
    return loads(patient.json(models_as_dict=False))


@patient_router.post("/id/{patient_id}")
async def update_patient_info_by_id(patient_id: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    requests.post(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}", json=dict(**update_object)).json()
    return await notify(f'/api/patients/id/{patient_id}')


@patient_router.post("/bed/{bed}")
async def update_patient_info_by_bed(bed: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    update_object = prepare_update_object(path, value)
    requests.post(f"http://medical_dal:8050/medical_dal/patient/bed/{bed}",
                  json=dict(**update_object)).json()
    return await notify(f'api/patients/bed/{bed}')
