from fastapi import APIRouter, Depends

from common.data_models.department import Department
from .auth import login_manager
from .wing import wing_router
from ..logics.utils import fetch_dal_json

department_router = APIRouter()

department_router.include_router(wing_router, prefix='/{department}/wings')


@department_router.get('/')
async def get_departments():
    return await fetch_dal_json("/departments/")


@department_router.get("/{department}", response_model=Department, response_model_exclude_unset=True)
async def get_department(department: str, _=Depends(login_manager)) -> dict:
    return await fetch_dal_json(f"/departments/{department}")
