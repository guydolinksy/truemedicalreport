import http
from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from sentry_sdk import capture_exception, capture_message

from common.data_models.department import Department
from common.data_models.image import Image
from common.data_models.labs import Laboratory
from common.data_models.measures import Measure
from common.data_models.medicine import Medicine
from common.data_models.patient import ExternalPatient, Intake
from common.data_models.referrals import Referral
from common.data_models.treatment import Treatment
from common.data_models.wing import WingSummary
from common.utilities.exceptions import PatientNotFound
from .wing import wing_router
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")

logger = logbook.Logger(__name__)


@department_router.get("/{department}", tags=["Department"], response_model=Department,
                       response_model_exclude_unset=True)
async def get_department(department: str, medical_dal_: MedicalDal = Depends(medical_dal)) -> Department:
    return Department(wings=[WingSummary(
        details=wing,
        filters=await medical_dal_.get_wing_filters(department, wing.key),
    ) for wing in await medical_dal_.get_department_wings(department)])


@department_router.post("/{department}/admissions", tags=["Department"])
async def update_admissions(department: str, admissions: List[ExternalPatient] = Body(..., embed=True),
                            dal: MedicalDal = Depends(medical_dal)):
    updated = {patient.external_id: patient for patient in admissions}
    existing = {patient.external_id: patient for patient in await dal.get_department_patients(department)}
    for patient_external_id in set(updated) | set(existing):
        await dal.upsert_patient(previous=existing.get(patient_external_id), patient=updated.get(patient_external_id))


@department_router.post("/{department}/measurements", tags=["Department"])
async def update_measurements(measurements: Dict[str, List[Measure]] = Body(..., embed=True),
                              dal: MedicalDal = Depends(medical_dal)):
    for patient in measurements:
        try:
            await dal.upsert_measurements(patient_id=patient, measures=measurements[patient])
        except PatientNotFound:
            msg = f"Cannot update patient {patient} measurements - Patient not found"
            capture_message(msg, level="warning")
            logger.debug(msg)
        except Exception as e:
            capture_exception(e, level="warning")
            logger.exception(f"update measurements failed - patient {patient} measurements {measurements[patient]}")


@department_router.post("/{department}/imaging")
async def update_imaging(department: str, images: Dict[str, List[Image]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for patient in images:
        for image in images[patient]:
            try:
                await dal.upsert_imaging(imaging_obj=image)
            except PatientNotFound:
                logger.debug('Cannot update patient {} images - Patient not found', patient)
            except Exception as e:
                logger.exception(f"update imaging failed - patient {patient} image {image}")


@department_router.post("/{department}/labs")
async def update_labs(labs: Dict[str, List[Laboratory]] = Body(..., embed=True),
                      dal: MedicalDal = Depends(medical_dal)):
    for patient in labs:
        try:
            logger.info(f"upsert labs for {patient}")
            await dal.upsert_labs(patient_id=patient, new_labs=labs[patient])
        except PatientNotFound:
            msg = f"Cannot update patient {patient} labs"
            capture_message(msg)
            logger.debug(msg)
        except Exception as e:
            capture_exception(e, level="warning")
            logger.exception(f"update labs failed - patient {patient}")


@department_router.post("/{department}/referrals")
async def update_referrals(department: str, referrals: Dict[str, List[Referral]] = Body(..., embed=True),
                           dal: MedicalDal = Depends(medical_dal)):
    _referral: Referral = None
    for patient in referrals:
        try:
            updated = {referral.external_id: referral for referral in referrals[patient]}
            existing = {referral.external_id: referral for referral in await dal.get_patient_referrals(patient)}
            for referral in set(updated) | set(existing):
                _referral = referral
                await dal.upsert_referral(
                    patient_id=patient,
                    previous=existing.get(referral),
                    referral=updated.get(referral)
                )

        except PatientNotFound:
            logger.debug('Cannot update patient {} referrals', patient)
        except Exception as e:
            logger.exception(f"update referrals failed - patient {patient}")


@department_router.post("/{department}/intake")
async def update_intake(department: str, intakes: Dict[str, Intake] = Body(..., embed=True),
                        dal: MedicalDal = Depends(medical_dal)):
    for patient, intake in intakes.items():
        try:
            await dal.upsert_intake(patient, intake)
        except PatientNotFound:
            logger.debug('Cannot update patient {} intake - Patient not found', patient)
        except Exception as e:
            logger.exception(f"update intake failed - intake {intake} patient {patient}")


@department_router.post("/{department}/treatments", status_code=http.HTTPStatus.OK)
async def update_treatments(department: str, treatments: Dict[str, Treatment] = Body(...),
                            dal: MedicalDal = Depends(medical_dal)):
    for record in treatments:
        try:
            await dal.upsert_treatment(record, treatments[record])
        except PatientNotFound:
            logger.debug('Cannot update patient {} treatments - Patient not found', record)
        except Exception as e:
            logger.exception(f"update treatments failed - record {record}")


@department_router.post("/{department}/medicines")
async def update_medicines(department: str, medications: Dict[str, List[Medicine]] = Body(...),
                           dal: MedicalDal = Depends(medical_dal)):
    for patient in medications:
        try:
            await dal.upsert_medicines(patient, medications[patient])
        except PatientNotFound:
            logger.debug('Cannot update patient {} medicines - Patient not found', patient)
