import http
from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.image import Image
from tmr_common.data_models.labs import Laboratory
from tmr_common.data_models.measures import Measure
from tmr_common.data_models.patient import ExternalPatient, Intake
from tmr_common.data_models.referrals import Referral
from tmr_common.data_models.treatment import Treatment
from tmr_common.data_models.department import Department
from tmr_common.data_models.wing import WingSummary
from tmr_common.utilities.exceptions import PatientNotFound
from .wing import wing_router
from .. import config
from ..dal.dal import MedicalDal

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")

logger = logbook.Logger(__name__)


# TODO remove duplicate use of dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient(**config.mongo_connection).medical)


@department_router.get("/{department}", tags=["Department"], response_model=Department,
                       response_model_exclude_unset=True)
def get_department(department: str, dal: MedicalDal = Depends(medical_dal)) -> Department:
    return Department(wings=[WingSummary(
        details=dal.get_wing(department, wing["key"]),
        filters=dal.get_wing_filters(department, wing["key"]),
    ) for wing in dal.get_department_wings(department)])


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
        except PatientNotFound:
            logger.debug('Cannot update patient {} measurements', patient)


@department_router.post("/{department}/imaging")
async def update_imaging(department: str, images: Dict[str, List[Image]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for patient in images:
        for image in images[patient]:
            try:
                await dal.upsert_imaging(imaging_obj=image)
            except PatientNotFound:
                logger.debug('Cannot update patient {} images', patient)


@department_router.post("/{department}/labs")
async def update_labs(labs: Dict[str, List[Laboratory]] = Body(..., embed=True),
                      dal: MedicalDal = Depends(medical_dal)):
    for patient in labs:
        try:
            await dal.upsert_labs(patient_id=patient, new_labs=labs[patient])
        except PatientNotFound:
            logger.debug('Cannot update patient {} labs', patient)


@department_router.post("/{department}/referrals")
async def update_referrals(department: str, referrals: Dict[str, List[Referral]] = Body(..., embed=True),
                           dal: MedicalDal = Depends(medical_dal)):
    for patient in referrals:
        for referral in referrals[patient]:
            try:
                await dal.upsert_referral(referral_obj=referral)
            except PatientNotFound:
                logger.debug('Cannot update patient {} referrals', patient)


@department_router.post("/{department}/intake")
async def update_intake(department: str, intakes: Dict[str, Intake] = Body(..., embed=True),
                        dal: MedicalDal = Depends(medical_dal)):
    for patient, intake in intakes.items():
        try:
            await dal.upsert_intake(patient, intake)
        except PatientNotFound:
            logger.debug('Cannot update patient {} intake', patient)


@department_router.post("/{department}/treatments", status_code=http.HTTPStatus.OK)
async def update_treatments(department: str, treatments: Dict[str, Treatment] = Body(...),
                            dal: MedicalDal = Depends(medical_dal)):
    for patient in treatments:
        try:
            await dal.upsert_treatment(patient, treatments[patient])
        except PatientNotFound:
            logger.debug('Cannot update patient {} treatments', patient)
