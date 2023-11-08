import logbook
from fastapi import APIRouter

from backend.logics.utils import fetch_dal_json

trauma_router = APIRouter()

logger = logbook.Logger(__name__)


@trauma_router.get('/images/{patient}')
async def get_images(patient: int):
    return await fetch_dal_json(f"/trauma/images/{patient}")


@trauma_router.get('/surgeries/{patient}')
async def get_surgeries(patient: int):
    return await fetch_dal_json(f"/trauma/surgeries/{patient}")


@trauma_router.get('/records')
async def get_records():
    return await fetch_dal_json(f"/trauma/trauma/records")
