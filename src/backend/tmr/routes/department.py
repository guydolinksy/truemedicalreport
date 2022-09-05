from typing import List

import requests
from fastapi import APIRouter, Depends

from tmr_common.data_models.department import Department
from .auth import manager
from .wing import wing_router

department_router = APIRouter()

department_router.include_router(wing_router, prefix='/{department}/wings')


@department_router.get("/{department}", response_model=Department, response_model_exclude_unset=True)
def get_department(department: str, _=Depends(manager)) -> Department:
    return requests.get(f"http://medical-dal/medical-dal/departments/{department}").json()
