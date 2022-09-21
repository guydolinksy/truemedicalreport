import logbook
from bson import ObjectId
from fastapi import APIRouter, Depends
from pymongo import MongoClient

from tmr_common.data_models.patient import Patient, PatientInfo
from tmr_common.data_models.admission import Admission
from .websocket import subscribe, notify
from .. import config
from ..dal.dal import MedicalDal

patient_router = APIRouter(tags=["Patient"])
logger = logbook.Logger(__name__)


# TODO remove duplicate use of dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient(**config.mongo_connection).medical)


@patient_router.get("/{patient}", response_model=Patient)
def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return dal.get_patient({'_id': ObjectId(patient)})


@patient_router.get("/{patient}/info", response_model=PatientInfo)
def get_patient_info_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> PatientInfo:
    return dal.get_patient_info({'_id': ObjectId(patient)})


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, update_object: dict,
                               dal: MedicalDal = Depends(medical_dal)) -> bool:
    return await dal.atomic_update_patient({'_id': ObjectId(patient)}, update_object)


@subscribe('.'.join([Patient.__name__, 'admission']))
async def on_admission_change(data: dict):
    key, old, new = data['key'], data['old'], data['new']
    if old:
        await notify(Admission.__name__, old)
    if new:
        await notify(Admission.__name__, new)
