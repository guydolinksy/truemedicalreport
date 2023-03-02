import logbook
from bson import ObjectId
from fastapi import APIRouter, Depends

from common.data_models.patient import Patient, PatientInfo
from common.data_models.plugins import PatientInfoPluginDataV1
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

patient_router = APIRouter(tags=["Patient"])
logger = logbook.Logger(__name__)


@patient_router.get("/{patient}", response_model=Patient)
async def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return await dal.get_patient({"_id": ObjectId(patient)})


@patient_router.get("/{patient}/info", response_model=PatientInfo)
async def get_patient_info_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> PatientInfo:
    return await dal.get_patient_info({"_id": ObjectId(patient)})


@patient_router.get("/{patient}/plugins/v1", response_model=PatientInfoPluginDataV1)
async def get_patient_info_plugin_data_by_id_v1(patient: str,
                                                dal: MedicalDal = Depends(medical_dal)) -> PatientInfoPluginDataV1:
    return await dal.get_patient_info_plugin_data_v1({"_id": ObjectId(patient)})


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, update_object: dict, dal: MedicalDal = Depends(medical_dal)) -> None:
    await dal.atomic_update_patient({"_id": ObjectId(patient)}, update_object)
