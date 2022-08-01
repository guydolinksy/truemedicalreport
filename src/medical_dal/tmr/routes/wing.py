from typing import List

import logbook
from fastapi import APIRouter, Depends
from pymongo import MongoClient

from tmr_common.data_models.bed import Bed
from tmr_common.data_models.patient import PatientNotifications
from tmr_common.data_models.wing import Wing, WingSummary
from ..dal.dal import MedicalDal

logger = logbook.Logger(__name__)
wing_router = APIRouter()


def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("mongo").medical)


@wing_router.get("/{wing}", response_model=WingSummary, response_model_exclude_unset=True, tags=["Wing"])
def get_wing_details(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    patients = dal.get_wing_patients(department, wing)
    details = dal.get_wing(department, wing)
    return WingSummary(patients=patients, details=details).dict(exclude_unset=True)


# TODO move logic to backend service after it works
@wing_router.get("/{wing}/notifications", tags=["Wing"], status_code=200)
def wing_notifications(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> \
        List[PatientNotifications]:
    return dal.get_wing_notifications(department, wing)


@wing_router.get("/{wing}/details", response_model=Wing, response_model_exclude_unset=True, tags=["Wing"])
def wing_details(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    res = dal.get_wing(department, wing)
    return Wing(oid=res["_id"]["$oid"], **res)


@wing_router.get("/{wing}/beds/{bed}", response_model=Bed, tags=["Wing"])
def get_patient_by_bed(department: str, wing: str, bed: str, dal: MedicalDal = Depends(medical_dal)) -> Bed:
    return Bed(patient=dal.get_patient_by_bed(department, wing, bed))
