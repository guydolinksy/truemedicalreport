import http
from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient
from werkzeug.exceptions import NotFound

from tmr_common.data_models.image import Image
from tmr_common.data_models.labs import Laboratory
from tmr_common.data_models.measures import Measure
from tmr_common.data_models.patient import ExternalPatient, BasicMedical
from tmr_common.data_models.referrals import Referral
from tmr_common.data_models.treatment import Treatment
from tmr_common.data_models.wing import WingOverview
from .wing import wing_router
from ..dal.dal import MedicalDal, Action

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")

logger = logbook.Logger(__name__)


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("mongo").medical)


@department_router.get("/{department}", tags=["Department"], response_model=List[WingOverview],
                       response_model_exclude_unset=True)
def get_department(department: str, dal: MedicalDal = Depends(medical_dal)) -> List[WingOverview]:
    return [WingOverview(
        oid=wing["_id"]["$oid"], **wing,
        patient_count=dal.get_wing_patient_count(department, wing["key"]),
        waiting_patient=10,
    ) for wing in dal.get_department_wings(department)]


@department_router.post("/{department}/admissions", tags=["Department"])
async def update_admissions(department: str, admissions: List[ExternalPatient] = Body(..., embed=True),
                            dal: MedicalDal = Depends(medical_dal)):
    updated = {patient.external_id: patient for patient in admissions}
    existing = {patient.external_id: patient for patient in dal.get_department_patients(department)}
    for patient in set(updated) | set(existing):
        await dal.upsert_patient(previous=existing.get(patient), patient=updated.get(patient))


@department_router.post("/{department}/measurements", tags=["Department"])
async def update_measurements(measurements: Dict[str, List[Measure]] = Body(..., embed=True),
                              dal: MedicalDal = Depends(medical_dal)):
    for patient in measurements:
        try:
            await dal.upsert_measurements(patient_id=patient, measures=measurements[patient])
        except NotFound:
            logger.exception('Cannot update patient {} measurements', patient)


@department_router.post("/{department}/imaging")
async def update_imaging(department: str, images: Dict[str, List[Image]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for patient in images:
        for image in images[patient]:
            try:
                await dal.upsert_imaging(imaging_obj=image)
            except NotFound:
                logger.exception('Cannot update patient {} images', patient)


@department_router.post("/{department}/labs")
async def update_labs(labs: Dict[str, List[Laboratory]] = Body(..., embed=True),
                      dal: MedicalDal = Depends(medical_dal)):
    for patient in labs:
        try:
            await dal.upsert_labs(patient_id=patient, new_labs=labs[patient])
        except NotFound:
            logger.exception('Cannot update patient {} labs', patient)


@department_router.post("/{department}/referrals")
async def update_referrals(department: str, referrals: Dict[str, List[Referral]] = Body(..., embed=True),
                           dal: MedicalDal = Depends(medical_dal)):
    for patient in referrals:
        for referral in referrals[patient]:
            try:
                await dal.upsert_referral(referral_obj=referral)
            except NotFound:
                logger.exception('Cannot update patient {} referrals', patient)


@department_router.post("/{department}/basic_medical")
async def update_basic_medical(department: str, basic_medicals: Dict[str, BasicMedical] = Body(..., embed=True),
                               dal: MedicalDal = Depends(medical_dal)):
    for patient, basic_medical in basic_medicals.items():
        try:
            await dal.upsert_basic_medical(patient, basic_medical)
        except NotFound:
            logger.exception('Cannot update patient {} basic medical', patient)


@department_router.post("/{department}/treatments", status_code=http.HTTPStatus.OK)
async def update_treatments(department: str, treatments: Dict[str, Treatment] = Body(...),
                            dal: MedicalDal = Depends(medical_dal)):
    for patient in treatments:
        try:
            await dal.upsert_treatment(patient, treatments[patient])
        except NotFound:
            logger.exception('Cannot update patient {} treatments', patient)


@department_router.get("/{department}/{wing}/waiting_labs", tags=["Department"], response_model=int,
                       response_model_exclude_unset=True)
def get_department_people_amount_waiting_labs(department: str, wing: str,
                                              dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.get_people_amount_waiting_labs(department, wing)


@department_router.get("/{department}/{wing}/waiting_nurse", tags=["Department"], response_model=int,
                       response_model_exclude_unset=True)
def get_department_people_amount_waiting_nurse(department: str, wing: str,
                                               dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.get_people_amount_waiting_nurse(department, wing)


@department_router.get("/{department}/{wing}/waiting_doctor", tags=["Department"], response_model=int,
                       response_model_exclude_unset=True)
def get_department_people_amount_waiting_doctor(department: str, wing: str,
                                                dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.get_people_amount_waiting_doctor(department, wing)


@department_router.get("/{department}/{wing}/waiting_imaging", tags=["Department"], response_model=int,
                       response_model_exclude_unset=True)
def get_department_people_amount_waiting_imaging(department: str, wing: str,
                                                 dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.get_people_amount_waiting_imaging(department, wing)


@department_router.get("/{department}/{wing}/waiting_referrals", tags=["Department"], response_model=int,
                       response_model_exclude_unset=True)
def get_department_people_amount_waiting_referrals(department: str, wing: str,
                                                   dal: MedicalDal = Depends(medical_dal)) -> int:
    return dal.get_people_amount_waiting_referrals(department, wing)
