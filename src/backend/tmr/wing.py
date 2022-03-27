from fastapi import APIRouter, Depends
from pymongo import MongoClient

from .src.dal import MedicalDal

wing_router = APIRouter()


def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("localhost").get_database("tmr").get_collection("patients"))


@wing_router.get("/{wing_id}/patient_count")
def patient_count(wing_id: int, dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.patient_count_in_wing(wing_id)
