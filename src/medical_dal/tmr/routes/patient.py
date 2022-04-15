from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.patient import Patient
from .websocket import notify
from ..dal.dal import MedicalDal

patient_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/{patient}", response_model=Patient)
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    patient_dal = dal.get_patient_by_id(patient)
    return Patient(oid=str(patient_dal.pop("_id")), **patient_dal)


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, update_object: dict,
                               dal: MedicalDal = Depends(medical_dal)) -> bool:
    res = dal.update_patient_by_id(patient, update_object)

    await notify_patient(patient)
    return res


@patient_router.post("/{patient}/warning")
async def warn_patient_by_id(patient: str, warning=Body(...), dal: MedicalDal = Depends(medical_dal)) -> bool:
    update_result = dal.append_warning_to_patient_by_id(patient, warning)
    if not update_result:
        return update_result

    return True


async def notify_patient(patient):
    await notify('patient', patient)
