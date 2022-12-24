import logbook
from fastapi import APIRouter, Depends

from .auth import login_manager
from ..logics.utils import fetch_dal_json

wing_router = APIRouter()

logger = logbook.Logger(__name__)


@wing_router.get("/{wing}")
async def get_wing_details(department: str, wing: str, _=Depends(login_manager)) -> dict:
    return await fetch_dal_json(f"/departments/{department}/wings/{wing}")


@wing_router.get("/{wing}/beds/{bed}")
async def get_patient_by_bed(department: str, wing: str, bed: str, _=Depends(login_manager)) -> dict:
    return await fetch_dal_json(f"/departments/{department}/wings/{wing}/beds/{bed}")
