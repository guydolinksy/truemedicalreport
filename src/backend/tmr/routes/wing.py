from fastapi import APIRouter
import requests

wing_router = APIRouter()


@wing_router.get("/{wing_id}/patient_count")
def patient_count(wing_id: str) -> int:
    return requests.get(f"http://medical_dal:8050/medical_dal/wing/{wing_id}/patient_count").json()


@wing_router.get("/{wing_id}")
def wing_structure_with_patient_info(wing_id: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/wing/{wing_id}").json()


@wing_router.get("/{wing_id}/details")
def wing_details(wing_id: str) -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/wing/{wing_id}/details").json()


@wing_router.get("/")
def get_all_wings_names() -> dict:
    return requests.get(f"http://medical_dal:8050/medical_dal/wing/").json()
