import logbook
from aiohttp.web_exceptions import HTTPError
from fastapi import APIRouter, Body, Depends

from common.data_models.patient import Patient, PanelPatient
from common.utilities.exceptions import PatientNotFound
from .auth import login_manager, user_settings
from .plugins import get_plugins
from ..logics.utils import prepare_update_object, fetch_dal_json, post_dal_json

patient_router = APIRouter()

logger = logbook.Logger(__name__)


@patient_router.get("/{patient}")
async def get_patient_by_id(patient: str, _=Depends(login_manager)) -> dict:
    try:
        p = await fetch_dal_json(f"/patients/{patient}")
        return Patient(**p).dict()
    except HTTPError as e:
        raise PatientNotFound() from e


@patient_router.get("/{patient}/info")
async def get_patient_info_by_id(
        patient: str, user=Depends(login_manager),
        user_settings_=Depends(user_settings)
) -> dict:
    try:
        res = await fetch_dal_json(f"/patients/{patient}/info")
    except HTTPError as e:
        raise PatientNotFound() from e

    plugins = [a async for a in get_plugins(patient, user, user_settings_)]

    return PanelPatient(**res, plugins=plugins).dict()


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value=Body(...), _=Depends(login_manager)) -> dict:
    update_object = prepare_update_object(path, value)
    return await post_dal_json(f"/patients/{patient}", dict(**update_object))


@patient_router.post("/{patient}/info")
async def update_patient_info_by_id(patient: str, path=Body(...), value=Body(...), _=Depends(login_manager)) -> dict:
    update_object = prepare_update_object(path, value)
    return await post_dal_json(f"/patients/{patient}", dict(**update_object))
