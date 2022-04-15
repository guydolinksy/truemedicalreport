from typing import List

from fastapi import APIRouter, Depends
from pymongo import MongoClient

from tmr_common.data_models.wing.wing import WingOverview
from .wing import wing_router
from ..dal.dal import MedicalDal

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@department_router.get("/{department}", response_model=List[WingOverview], response_model_exclude_unset=True)
def get_department(department: str, dal: MedicalDal = Depends(medical_dal)) -> List[WingOverview]:
    return [WingOverview(
        oid=wing["_id"]["$oid"], **wing,
        patient_count=dal.get_wing_patient_count(department, wing["key"]),
        waiting_patient=10,
    ) for wing in dal.get_department_wings(department)]
