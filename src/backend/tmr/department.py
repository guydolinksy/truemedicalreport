from fastapi import APIRouter, Depends
from pymongo import MongoClient

from .src.dal import MedicalDal

department_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@department_router.get("/")
def get_department_overview(dal: MedicalDal = Depends(medical_dal)) -> dict:
    wings_data = dal.get_all_wings_names()
    for wing in wings_data:
        patient_count = dal.patient_count_in_wing(wing["_id"]["$oid"])
        wing["patient_count"] = patient_count
        wing["waiting_petient"] = int(patient_count / 2)
    return wings_data
