from typing import Optional, Any

import logbook
from bson import ObjectId
from fastapi import APIRouter, Depends, Body

from common.data_models.patient import Patient
from common.data_models.plugin import PatientInfoPluginDataV1
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

patient_router = APIRouter(tags=["Patient"])
logger = logbook.Logger(__name__)


@patient_router.get("/{patient}", response_model=Patient)
async def get_patient_by_id(patient: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    return await dal.get_patient({"_id": ObjectId(patient)})


@patient_router.get("/{patient}/plugins/v1", response_model=PatientInfoPluginDataV1)
async def get_patient_info_plugin_data_by_id_v1(patient: str,
                                                dal: MedicalDal = Depends(medical_dal)) -> PatientInfoPluginDataV1:
    return await dal.get_patient_info_plugin_data_v1({"_id": ObjectId(patient)})


@patient_router.post("/{patient}")
async def update_patient_by_id(patient: str, path=Body(...), value: Any = Body(default=None),
                               type_: str | bool = Body(...), dal: MedicalDal = Depends(medical_dal)) -> None:
    await dal.update_patient({"_id": ObjectId(patient)}, path=path, value=value, type_=type_)
    return {}
