import logbook
from fastapi import APIRouter, Depends
from pymongo import MongoClient

from tmr_common.data_models.bed import Bed

from tmr_common.data_models.wing import Wing, WingSummarize
from ..dal.dal import MedicalDal

logger = logbook.Logger(__name__)
wing_router = APIRouter()


def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@wing_router.get("/{wing}", response_model=WingSummarize, response_model_exclude_unset=True, tags=["Wing"])
def get_wing_details(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    patients = dal.get_wing_patients(department, wing)
    details = dal.get_wing(department, wing)
    return WingSummarize(patients=patients, details=details).dict(exclude_unset=True)


@wing_router.get("/{wing}/notifications", tags=["Wing"])
def wing_notifications(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> list:
    patients = []
    for patient in dal.get_wing_patients(department, wing):
        notification_patient = {
            "patient": {'name': patient.name, "oid": patient.oid},
            "messages": patient.messages,
        }
        if patient.messages:
            for message in patient.messages:
                if message.get("danger"):
                    notification_patient["danger"] = True
                    patients.append(notification_patient)
                    break
    return sorted(patients, key=lambda patient_obj: patient_obj["patient"]["name"])


@wing_router.get("/{wing}/details", response_model=Wing, response_model_exclude_unset=True, tags=["Wing"])
def wing_details(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    res = dal.get_wing(department, wing)
    return Wing(oid=res["_id"]["$oid"], **res)


@wing_router.get("/{wing}/beds/{bed}", response_model=Bed, tags=["Wing"])
def get_patient_by_bed(department: str, wing: str, bed: str, dal: MedicalDal = Depends(medical_dal)) -> Bed:
    return Bed(patient=dal.get_patient_by_bed(department, wing, bed))
