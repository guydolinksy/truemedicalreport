from fastapi import APIRouter, Depends
from pymongo import MongoClient
from typing import List
from data_models.patient_count import PatientCount
from data_models.wing.wing import Wing, WingOverview
from ..dal.dal import MedicalDal

department_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@department_router.get("/", response_model=List[WingOverview], response_model_exclude_unset=True)
def get_department_overview(dal: MedicalDal = Depends(medical_dal)) -> List[WingOverview]:
    return [
        WingOverview(
            oid=wing["_id"]["$oid"], **wing,
            patient_count=dal.patient_count_in_wing(wing_id=wing["_id"]["$oid"]),
            waiting_patient=PatientCount(
                patient_count=dal.patient_count_in_wing(wing_id=wing["_id"]["$oid"]).patient_count / 2))
            .dict(exclude_unset=True)
        for wing in dal.get_all_wings_names()
    ]
