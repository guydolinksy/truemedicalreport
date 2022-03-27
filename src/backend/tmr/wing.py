from fastapi import APIRouter, Depends
from pymongo import MongoClient

from .src.dal import MedicalDal

wing_router = APIRouter()


def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@wing_router.get("/{wing_id}/patient_count")
def patient_count(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.patient_count_in_wing(wing_id)


@wing_router.get("/{wing_id}/patients")
def patients_in_wing(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.patients_in_wing(wing_id)


@wing_router.get("/{wing_id}/details")
def wing_details(wing_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.get_wing_details(wing_id)
