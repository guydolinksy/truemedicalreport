import logbook
from bson import ObjectId
from fastapi import APIRouter, Depends
from pymongo import MongoClient

from tmr_common.data_models.patient import Patient, PatientInfo
from ..dal.dal import MedicalDal

patient_router = APIRouter(tags=["Patient"])
logger = logbook.Logger(__name__)


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("mongo").medical)


@patient_router.get("/{patient}", response_model=Patient)
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return dal.get_patient({'_id': ObjectId(patient)})


@patient_router.get("/{patient}/info", response_model=PatientInfo)
def get_patient_info_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> PatientInfo:
    return dal.get_patient_info({'_id': ObjectId(patient)})


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, update_object: dict,
                               dal: MedicalDal = Depends(medical_dal)) -> bool:
    return await dal.update_patient({'_id': ObjectId(patient)}, update_object)

