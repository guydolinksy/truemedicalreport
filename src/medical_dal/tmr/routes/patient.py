import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.notification import Notification
from tmr_common.data_models.patient import Patient, PatientInfo
from ..dal.dal import MedicalDal, Action

patient_router = APIRouter(tags=["Patient"])
logger = logbook.Logger(__name__)


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("mongo").medical)


@patient_router.get("/{patient}", response_model=Patient)
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return dal.get_patient_by_id(patient)


@patient_router.get("/{patient}/info", response_model=PatientInfo)
def get_patient_info_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> PatientInfo:
    return dal.get_patient_info_by_id(patient)


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, update_object: dict,
                               dal: MedicalDal = Depends(medical_dal)) -> bool:
    return await dal.update_patient_by_id(patient, update_object)


@patient_router.post("/{patient}/warning")
async def warn_patient_by_id(patient: str, warning=Body(...), dal: MedicalDal = Depends(medical_dal)) -> bool:
    update_result = dal.append_warning_to_patient_by_id(patient, warning)
    if not update_result:
        return update_result

    return True
