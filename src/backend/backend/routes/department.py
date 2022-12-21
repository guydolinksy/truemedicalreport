import requests
from fastapi import APIRouter, Depends

from common.data_models.department import Department
from .auth import login_manager
from .wing import wing_router
from .. import config

department_router = APIRouter()

department_router.include_router(wing_router, prefix='/{department}/wings')


@department_router.get("/{department}", response_model=Department, response_model_exclude_unset=True)
def get_department(department: str, _=Depends(login_manager)) -> Department:
    return requests.get(f"{config.dal_url}/departments/{department}").json()
