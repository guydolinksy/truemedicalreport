import logbook
import requests
from fastapi import APIRouter, Depends

from .auth import login_manager
from .. import config

wing_router = APIRouter()

logger = logbook.Logger(__name__)


@wing_router.get("/{wing}")
def get_wing_details(department: str, wing: str, _=Depends(login_manager)) -> dict:
    res = requests.get(f"{config.dal_url}/departments/{department}/wings/{wing}").json()
    return res


@wing_router.get("/{wing}/beds/{bed}")
def get_patient_by_bed(department: str, wing: str, bed: str, _=Depends(login_manager)) -> dict:
    res = requests.get(f"{config.dal_url}/departments/{department}/wings/{wing}/beds/{bed}").json()
    return res
