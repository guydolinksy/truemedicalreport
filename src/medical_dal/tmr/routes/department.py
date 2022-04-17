from typing import List

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.measures import Measures
from tmr_common.data_models.patient import Patient
from tmr_common.data_models.wing import WingOverview
from .patient import upsert_patient
from .wing import wing_router
from ..dal.dal import MedicalDal, Action

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
async def update_admissions(department: str, admissions=Body(..., embed=True), dal: MedicalDal = Depends(medical_dal)):
    for wing in dal.get_department_wings(department):
        patients = {patient.id_: patient for patient in dal.get_wing_patients(department, wing['key'])}
        existing, queried = set(patients), set(admissions)
        for patient in existing - queried:
            await upsert_patient(patient=patients[patient], dal=dal, action=Action.remove)
        for patient in queried - existing:
            await upsert_patient(patient=admissions[patient], dal=dal, action=Action.insert)
        for patient in queried & existing:
            await upsert_patient(patient=admissions[patient], dal=dal, action=Action.update)


@department_router.post("/{department}/measurements")
def update_measurements(department: str, measurements=Body(..., embed=True), dal: MedicalDal = Depends(medical_dal)):
    for patient in measurements:
        logger.debug(Measures(**measurements[patient]))
