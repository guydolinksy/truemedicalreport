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


@wing_router.get("/{wing}", response_model=WingSummarize, response_model_exclude_unset=True)
def get_wing_details(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    patients = dal.get_wing_patients(department, wing)
    details = dal.get_wing(department, wing)
    return WingSummarize(patients=patients, details=details).dict(exclude_unset=True)


@wing_router.get("/{wing}/notifications")
def wing_notifications(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> list:
    # print([patient for patient in dal.get_wing_patients(department, wing)])
    # logger.debug([{
    #     'patient': {'name': patient.name, 'oid': patient.oid},
    #     'danger': True,
    #     'messages': patient.messages[0] #[{'danger': patient.messages[0]["danger"], 'content': patient.messages[0]["content"]}]
    # } for (i, patient) in enumerate(dal.get_wing_patients(department, wing))])
    patients = []
    for patient in dal.get_wing_patients(department, wing):
        notification_object = {patient: {'name': patient.name, "oid": patient.oid},
                               'danger': bool(filter(lambda message: message.get("danger") == True,patient.messages if patient.messages else [])),
                               'messages': patient.messages}
        patients.append(notification_object)
    return patients


@wing_router.get("/{wing}/details", response_model=Wing, response_model_exclude_unset=True)
def wing_details(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    res = dal.get_wing(department, wing)
    return Wing(oid=res["_id"]["$oid"], **res)


@wing_router.get("/{wing}/beds/{bed}", response_model=Bed)
def get_patient_by_bed(department: str, wing: str, bed: str, dal: MedicalDal = Depends(medical_dal)) -> Bed:
    return Bed(patient=dal.get_patient_by_bed(department, wing, bed))
