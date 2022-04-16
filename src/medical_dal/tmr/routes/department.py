from typing import List

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient
from starlette.responses import Response

from tmr_common.data_models.measures import Measures
from tmr_common.data_models.patient import Patient
from tmr_common.data_models.wing import WingOverview
from .wing import wing_router
from ..dal.dal import MedicalDal

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")

logger = logbook.Logger(__name__)


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


@department_router.post("/{department}/admissions")
def update_admissions(response: Response, department: str, body=Body(...), dal: MedicalDal = Depends(medical_dal)):
    for patient in body['admissions']:
        logger.debug(Patient(**patient))


@department_router.post("/{department}/measurements")
def update_measurements(response: Response, department: str, body=Body(...), dal: MedicalDal = Depends(medical_dal)):
    for patient in body['measurements']:
        logger.debug(Measures(**body['measurements'][patient]))
