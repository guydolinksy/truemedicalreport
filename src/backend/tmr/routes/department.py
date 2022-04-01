from fastapi import APIRouter
import requests
from tmr_common.data_models.wing.wing import WingOverview
from typing import List

department_router = APIRouter()


@department_router.get("/", response_model=List[WingOverview], response_model_exclude_unset=True)
def get_department_overview() -> List[WingOverview]:
    return requests.get(f"http://medical_dal:8050/medical_dal/department/").json()
