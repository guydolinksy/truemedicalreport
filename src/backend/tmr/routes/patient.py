from fastapi import APIRouter, Body
import requests

from .websocket import notify

patient_router = APIRouter()


@patient_router.get("/bed/{bed}")
def get_patient_info_by_id(bed: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/patient/bed/{bed}").json()


@patient_router.get("/id/{patient_id}")
def get_patient_info_by_id(patient_id: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}").json()


@patient_router.post("/id/{patient_id}")
async def update_patient_info_by_id(patient_id: str, path=Body(...), value=Body(...), data=Body(...)) -> dict:
    requests.post(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}", json=dict(
        path=path, value=value, data=data
    )).json()
    return await notify(f'/api/patients/id/{patient_id}')
