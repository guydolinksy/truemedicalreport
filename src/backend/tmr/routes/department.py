from fastapi import APIRouter, Depends
import requests

from ..logics.auth import manager
from tmr_common.data_models.wing.wing import WingOverview
from typing import List

department_router = APIRouter()


@department_router.get("/", response_model=List[WingOverview], response_model_exclude_unset=True)
def get_department_overview(user=Depends(manager)) -> List[WingOverview]:
    return requests.get(f"http://medical-dal/medical-dal/department/").json()
