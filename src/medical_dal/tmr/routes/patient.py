import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.patient import Patient
from ..dal.dal import MedicalDal, Action

patient_router = APIRouter()
logger = logbook.Logger(__name__)


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/{patient}", response_model=Patient)
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return dal.get_patient_by_id(patient)


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, update_object: dict,
                               dal: MedicalDal = Depends(medical_dal)) -> bool:
    return await dal.update_patient_by_id(patient, update_object)


@patient_router.post("/{action}")
async def upsert_patient(action: Action, patient: Patient = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)) -> bool:
    return await dal.upsert_patient(patient, action)


@patient_router.post("/{patient}/warning")
async def warn_patient_by_id(patient: str, warning=Body(...), dal: MedicalDal = Depends(medical_dal)) -> bool:
    update_result = dal.append_warning_to_patient_by_id(patient, warning)
    if not update_result:
        return update_result

    return True

