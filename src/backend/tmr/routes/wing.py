from json import loads

import requests
from fastapi import APIRouter, Depends

from tmr_common.data_models.patient import Patient
from ..logics.auth import manager

wing_router = APIRouter()


@wing_router.get("/{wing}")
def get_wing_details(department: str, wing: str, _=Depends(manager)) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}").json()
    return res


@wing_router.get("/{wing}/notifications")
def wing_notifications(department: str, wing: str, _=Depends(manager)) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}/notifications").json()
    return res


@wing_router.get("/{wing}/beds/{bed}")
def get_patient_by_bed(department: str, wing: str, bed: str) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}/beds/{bed}").json()
    return res
