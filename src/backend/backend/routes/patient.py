from typing import Optional, Any

import logbook
from aiohttp.web_exceptions import HTTPError
from fastapi import APIRouter, Body, Depends

from common.data_models.patient import Patient
from common.data_models.plugin import PanelPatient
from common.utilities.exceptions import PatientNotFoundException
from .auth import login_manager, user_settings
from .plugins import get_plugins
from ..logics.utils import prepare_update_object, fetch_dal_json, post_dal_json

patient_router = APIRouter()

logger = logbook.Logger(__name__)


@patient_router.get("/{patient}")
async def get_patient_by_id(patient: str, _=Depends(login_manager)) -> dict:
    try:
        p = await fetch_dal_json(f"/patients/{patient}")
        return Patient(**p).model_dump()
    except HTTPError as e:
        raise PatientNotFoundException() from e


@patient_router.get("/{patient}/info")
async def get_patient_info_by_id(
        patient: str, user=Depends(login_manager),
        user_settings_=Depends(user_settings)
) -> dict:
    try:
        res = await fetch_dal_json(f"/patients/{patient}")
    except HTTPError as e:
        raise PatientNotFoundException() from e

    plugins = [a async for a in get_plugins(patient, user, user_settings_)]

    return PanelPatient(**res, plugins=plugins).model_dump()


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value: Any = Body(default=None),
                               type_: str | bool = Body(...), _=Depends(login_manager)) -> dict:
    return await post_dal_json(f"/patients/{patient}", json_payload=dict(path=path, value=value, type_=type_))


@patient_router.post("/{patient}/info")
async def update_patient_info_by_id(patient: str, path=Body(...), value=Body(...), type_: str | bool = Body(..., ),
                                    _=Depends(login_manager)) -> dict:
    return await post_dal_json(f"/patients/{patient}", json_payload=dict(path=path, value=value, type_=type_))
