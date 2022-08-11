import logbook
import requests
from fastapi import APIRouter, Depends

from .auth import manager

wing_router = APIRouter()

logger = logbook.Logger(__name__)


@wing_router.get("/{wing}")
def get_wing_details(department: str, wing: str, _=Depends(manager)) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}").json()
    return res


@wing_router.get("/{wing}/status")
def wing_status(department: str, wing: str, _=Depends(manager)) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}/status").json()
    return res


@wing_router.get("/{wing}/beds/{bed}")
def get_patient_by_bed(department: str, wing: str, bed: str) -> dict:
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}/beds/{bed}").json()
    return res
