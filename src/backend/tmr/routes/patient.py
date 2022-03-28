from fastapi import APIRouter
import requests

patient_router = APIRouter()


@patient_router.get("/bed/{bed}")
def get_patient_info_by_id(bed: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/patient/bed/{bed}").json()


@patient_router.get("/id/{patient_id}")
def get_patient_info_by_id(patient_id: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/patient/id/{patient_id}").json()
