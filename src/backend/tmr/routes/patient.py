from fastapi import APIRouter, Body
import requests
from tmr_common.data_models.patient import Patient
from tmr_common.data_models.measures.measures import Measures

from .websocket import notify

patient_router = APIRouter()


@patient_router.get("/bed/{bed}", response_model=Patient, response_model_exclude_unset=True)
def get_patient_info_by_id(bed: str) -> Patient:
    return Patient(**requests.get(f"http://medical_dal:8050/medical_dal/patient/bed/{bed}").json())


@patient_router.get("/id/{patient_id}")
def get_patient_info_by_id(patient_id: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}").json()


@patient_router.get("/{patient_id}/measures")
def get_patient_measures(patient_id: str) -> Measures:
    return Measures(requests.get(f"http://medical_dal:8050/medical_dal/patient/{patient_id}").json())


@patient_router.post("/id/{patient_id}")
async def update_patient_info_by_id(patient_id: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    requests.post(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}", json=dict(
        path=path, value=value, data=data
    )).json()
    return await notify(f'/api/patients/id/{patient_id}')
