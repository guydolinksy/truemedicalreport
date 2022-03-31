from fastapi import APIRouter
import requests
from data_models.patient_count import PatientCount
from data_models.wing.wing import Wing, WingSummarize
from typing import List

wing_router = APIRouter()


@wing_router.get("/{wing_id}/patient_count", response_model=PatientCount)
def patient_count(wing_id: str) -> PatientCount:
    return PatientCount(
        **requests.get(f"http://medical_dal:8050/medical_dal/wing/{wing_id}/patient_count").json())


@wing_router.get("/{wing_id}", response_model=WingSummarize, response_model_exclude_unset=True)
def wing_structure_with_patient_info(wing_id: str) -> WingSummarize:
    return WingSummarize(**requests.get(f"http://medical_dal:8050/medical_dal/wing/{wing_id}").json())


@wing_router.get("/{wing_id}/details", response_model=Wing)
def wing_details(wing_id: str) -> Wing:
    response = requests.get(f"http://medical_dal:8050/medical_dal/wing/{wing_id}/details").json()
    return Wing(**response)


@wing_router.get("/", response_model=List[Wing], response_model_include={"name", "oid"})
def get_all_wings_names() -> List[Wing]:
    wings = requests.get(f"http://medical_dal:8050/medical_dal/wing/").json()
    return wings
