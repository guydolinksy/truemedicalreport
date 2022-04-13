from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from .websocket import notify
from ..dal.dal import MedicalDal
from tmr_common.data_models.patient import Patient
from tmr_common.data_models.measures.measures import Measures

patient_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/bed/{bed}", response_model=Patient)
def get_patient_brief_by_bed(bed: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    patient_dal = dal.get_patient_info_by_bed(bed)
    return Patient(oid=patient_dal["_id"]["$oid"], wing=patient_dal["wing_id"]["$oid"], **patient_dal)


@patient_router.get("/id/{patient_id}", response_model=Patient)
def get_patient_brief_by_id(patient_id: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    patient_dal = dal.get_patient_info_by_id(patient_id)
    return Patient(oid=patient_dal["_id"]["$oid"], wing=patient_dal["wing_id"]["$oid"], **patient_dal)


@patient_router.get("/{patient_id}/measures", response_model=Measures)
def get_patient_measures(patient_id: str, dal: MedicalDal = Depends(medical_dal)) -> Measures:
    return Measures(**dal.get_patient_measures(patient_id)["measures"])


@patient_router.post("/id/{patient_id}")
async def update_patient_brief_by_id(patient_id: str, update_object: dict,
                                     dal: MedicalDal = Depends(medical_dal)) -> bool:
    dal.update_patient_info_by_id(patient_id, update_object)

    await notify_patient(dal, patient_id)
    return True


@patient_router.post("/bed/{bed}")
async def update_patient_brief_by_bed(bed: str, update_object: dict, dal: MedicalDal = Depends(medical_dal)) -> bool:
    dal.update_patient_info_by_bed(bed, update_object)

    patient_dal = dal.get_patient_info_by_bed(bed)
    await notify_patient(dal, patient_dal["_id"]["$oid"], bed)
    return True


@patient_router.post("/id/{patient_id}/warning")
async def warn_patient_by_id(patient_id: str, warning=Body(...), dal: MedicalDal = Depends(medical_dal)) -> bool:
    update_result = dal.append_warning_to_patient_by_id(patient_id, warning)
    if not update_result:
        return update_result

    return True


async def notify_patient(dal, patient_id, bed=None):
    await notify('patient_id', patient_id)
    await notify('patient_info', patient_id)
    if bed is None:
        patient_dal = dal.get_patient_info_by_id(patient_id)
        bed = patient_dal['bed']
    if bed:
        await notify('patient_bed', bed)
