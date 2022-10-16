import logbook
import requests
from fastapi import APIRouter, Body, Depends

from ..logics.utils import prepare_update_object
from common.data_models.patient import Patient, PanelPatient, PatientInfoPlugin
from common.utilities.exceptions import PatientNotFound
from .auth import login_manager, user_settings
from .. import config
from ..logics.settings import general_settings

patient_router = APIRouter()

logger = logbook.Logger(__name__)


@patient_router.get("/{patient}")
def get_patient_by_id(patient: str, _=Depends(login_manager)) -> dict:
    res = requests.get(f"{config.dal_url}/patients/{patient}")
    if not res.ok:
        raise PatientNotFound()
    return Patient(**res.json()).dict()


@patient_router.get("/{patient}/info")
def get_patient_info_by_id(patient: str, general_settings_=Depends(general_settings),
                           user_settings_=Depends(user_settings)) -> dict:
    res = requests.get(f"{config.dal_url}/patients/{patient}/info")
    if not res.ok:
        raise PatientNotFound()
    plugins = getattr(general_settings_, 'plugins', {})
    user_plugins = getattr(user_settings_, 'plugins', {})
    plugins = [PatientInfoPlugin(key=p, **plugins[p]) for p in plugins if user_plugins.get(p, {}).get('enabled', True)]

    return PanelPatient(**res.json(), plugins=plugins).dict()


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...),
                               _=Depends(login_manager)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"{config.dal_url}/patients/{patient}", json=dict(**update_object)).json()


@patient_router.post("/{patient}/info")
async def update_patient_info_by_id(patient: str, path=Body(...), value=Body(...), data=Body(...),
                                    _=Depends(login_manager)) -> dict:
    update_object = prepare_update_object(path, value)
    return requests.post(f"{config.dal_url}/patients/{patient}", json=dict(**update_object)).json()
