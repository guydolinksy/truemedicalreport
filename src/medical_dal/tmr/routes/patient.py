from fastapi import APIRouter, Depends
from pymongo import MongoClient

from ..dal.dal import MedicalDal
from data_models.patient import Patient
from data_models.measures.measures import Measures

patient_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/bed/{bed}", response_model=Patient)
def get_patient_info_by_bed(bed: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    patient_dal = dal.get_patient_info_by_bed(bed)
    return Patient(oid=patient_dal["_id"]["$oid"],
                   wing=patient_dal["wing_id"]["$oid"], **patient_dal)


@patient_router.get("/id/{patient_id}", response_model=Patient)
def get_patient_info_by_id(patient_id: str, dal: MedicalDal = Depends(medical_dal)) -> Patient:
    patient_dal = dal.get_patient_info_by_id(patient_id)
    return Patient(oid=patient_dal["_id"]["$oid"],
                   wing=patient_dal["wing_id"]["$oid"], **patient_dal)


@patient_router.get("/{patient_id}/measures", response_model=Measures)
def get_patient_measures(patient_id: str, dal: MedicalDal = Depends(medical_dal)) -> Measures:
    return Measures(**dal.get_patient_measures(patient_id)["measures"])
