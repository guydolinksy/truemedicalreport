from fastapi import APIRouter, Depends
from pymongo import MongoClient
from bson.json_util import dumps
from data_models.wing.wing import Wing, WingSummarize
from data_models.patient_count import PatientCount
from ..dal.dal import MedicalDal
from typing import List

wing_router = APIRouter()


def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@wing_router.get("/{wing_id}/patient_count", response_model=PatientCount, response_model_exclude_unset=True)
def patient_count(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> PatientCount:
    return dal.patient_count_in_wing(wing_id)


@wing_router.get("/{wing_id}", response_model=WingSummarize, response_model_exclude_unset=True)
def wing_structure_with_patient_info(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    patients = dal.patients_in_wing(wing_id)
    wing_structure = dal.get_wing_details(wing_id)
    return WingSummarize(patients_beds=patients, structure=wing_structure).dict(exclude_unset=True)


@wing_router.get("/{wing_id}/details", response_model=Wing, response_model_exclude_unset=True)
def wing_details(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    res = dal.get_wing_details(wing_id)
    return Wing(oid=res["_id"]["$oid"], **res)
