from fastapi import APIRouter, Depends
from pymongo import MongoClient

from .src.dal import MedicalDal

patient_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/{patient_id}")
def get_patient_info_by_id(patient_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.get_patient_info_by_id(patient_id)
