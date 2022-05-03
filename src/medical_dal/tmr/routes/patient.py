import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient
import json

from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.patient import Patient, ExternalPatient, PatientInfo
from tmr_common.data_models.notification import Notification

from ..dal.dal import MedicalDal, Action

patient_router = APIRouter()
logger = logbook.Logger(__name__)


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/{patient}", response_model=Patient, tags=["Patient"])
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return dal.get_patient_by_id(patient)


@patient_router.get("/{patient}/info", response_model=PatientInfo, tags=["PatientInfo"])
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> PatientInfo:
    return dal.get_patient_info_by_id(patient)


@patient_router.post("/{patient}", tags=["Patient"])
async def update_patient_by_id(patient: str, update_object: dict,
                               dal: MedicalDal = Depends(medical_dal)) -> bool:
    return await dal.update_patient_by_id(patient, update_object)


@patient_router.post("/{patient}/warning", tags=["Patient"])
async def warn_patient_by_id(patient: str, warning=Body(...), dal: MedicalDal = Depends(medical_dal)) -> bool:
    update_result = dal.append_warning_to_patient_by_id(patient, warning)
    if not update_result:
        return update_result

    return True


@patient_router.post("/{patient}/notification", tags=["Patient"], status_code=201)
async def add_notification_to_patient(patient: str, notification: Notification = Body(..., embed=True),
                                      dal: MedicalDal = Depends(medical_dal)):
    await dal.upsert_notification(patient_id=patient, notification=notification, action=Action.insert)
