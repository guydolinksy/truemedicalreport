from fastapi import APIRouter, Depends
from pymongo import MongoClient
from bson.json_util import dumps

from ..dal.dal import MedicalDal

wing_router = APIRouter()


def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@wing_router.get("/{wing_id}/patient_count")
def patient_count(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.patient_count_in_wing(wing_id)


@wing_router.get("/{wing_id}")
def wing_structure_with_patient_info(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    patients = dal.patients_in_wing(wing_id)
    wing_structure = dal.get_wing_details(wing_id)
    return dict(patients=patients, structure=wing_structure)


@wing_router.get("/{wing_id}/details")
def wing_details(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.get_wing_details(wing_id)


@wing_router.get("/")
def get_all_wings_names(dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.get_all_wings_names()
