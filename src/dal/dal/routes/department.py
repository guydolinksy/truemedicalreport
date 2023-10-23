from typing import List, Dict, Optional

import logbook
from fastapi import APIRouter, Depends, Body
from sentry_sdk import capture_exception, capture_message

from common.data_models.department import Department
from common.data_models.discussion import Note
from common.data_models.image import Image
from common.data_models.labs import LabCategory
from common.data_models.measures import Measure
from common.data_models.medication import Medication
from common.data_models.patient import ExternalData, Intake
from common.data_models.referrals import Referral
from common.data_models.wing import Wing
from common.utilities.exceptions import PatientNotFoundException, DepartmentNotFoundException
from .wing import wing_router
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")

logger = logbook.Logger(__name__)


@department_router.get('/')
async def get_departments(medical_dal_: MedicalDal = Depends(medical_dal)) -> List[Department]:
    return [d async for d in medical_dal_.get_departments()]


@department_router.post('/mci/intake')
async def intake_mci_patients(intake: List[str] = Body(..., embed=True),
                              medical_dal_: MedicalDal = Depends(medical_dal)) -> None:
    logger.debug('MCI {} ', intake)
    return await medical_dal_.update_mci_patients(intake)


@department_router.get("/{department}")
async def get_department(department: str, medical_dal_: MedicalDal = Depends(medical_dal)) -> Department:
    async for d in medical_dal_.get_departments():
        if d.key == department:
            return d
    else:
        raise DepartmentNotFoundException()


@department_router.post("/{department}/admissions")
async def update_admissions(department: str, admissions: List[ExternalData] = Body(..., embed=True),
                            dal: MedicalDal = Depends(medical_dal)):
    updated = {patient.external_id: patient for patient in admissions}
    existing = {patient.external_id async for _, patient in dal.get_patients({"admission.department_id": department})}
    for patient_external_id in set(updated):
        await dal.upsert_admission(
            external_id=patient_external_id,
            patient=updated.get(patient_external_id),
        )
    for patient_external_id in existing - set(updated):
        logger.debug('DROPPING {}', patient_external_id)
        await dal.upsert_admission(external_id=patient_external_id, patient=None)


@department_router.post("/{department}/measurements", tags=["Department"])
async def update_measurements(measurements: Dict[str, List[Measure]] = Body(..., embed=True),
                              dal: MedicalDal = Depends(medical_dal)):
    for patient in measurements:
        try:
            await dal.upsert_measurements(patient_id=patient, measures=measurements[patient])
        except PatientNotFoundException:
            msg = f"Cannot update patient {patient} measurements - Patient not found"
            capture_message(msg, level="warning")
            logger.debug(msg)
        except Exception as e:
            capture_exception(e, level="warning")
            logger.exception(f"update measurements failed - patient {patient} measurements {measurements[patient]}")


@department_router.post("/{department}/imaging")
async def update_imaging(department: str, images: Dict[str, Dict[str, Image]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for patient in images:
        try:
            await dal.upsert_imaging(patient, images=images[patient])
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} images - Patient not found', patient)
        except Exception:
            logger.exception(f"update imaging failed - patient {patient}")


@department_router.post("/{department}/referrals")
async def update_referrals(department: str, at: str = Body(..., embed=True),
                           referrals: Dict[str, Dict[str, Referral]] = Body(..., embed=True),
                           dal: MedicalDal = Depends(medical_dal)):
    for patient in set(referrals) | {p.external_id async for _, p in
                                     dal.get_patients({"admission.department_id": department})}:
        try:
            await dal.upsert_referral(patient_id=patient, at=at, referrals=referrals.get(patient, {}))
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} referrals', patient)
        except Exception as e:
            logger.exception(f"update referrals failed - patient {patient}")


@department_router.post("/{department}/labs")
async def update_labs(labs: Dict[str, Dict[str, LabCategory]] = Body(..., embed=True),
                      dal: MedicalDal = Depends(medical_dal)):
    for patient in labs:
        try:
            logger.info(f"upsert labs for {patient}")
            await dal.upsert_labs(patient_id=patient, labs=labs[patient])
        except PatientNotFoundException:
            msg = f"Cannot update patient {patient} labs"
            capture_message(msg)
            logger.debug(msg)
        except Exception as e:
            capture_exception(e, level="warning")
            logger.exception(f"update labs failed - patient {patient}")


@department_router.post("/{department}/intake_nurse")
async def update_intake_nurse(department: str, intakes: Dict[str, Intake] = Body(..., embed=True),
                              dal: MedicalDal = Depends(medical_dal)):
    for patient, intake in intakes.items():
        try:
            await dal.upsert_intake_nurse(patient, intake)
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} intake nurse - Patient not found', patient)
        except Exception as e:
            logger.exception(f"update intake failed - intake nurse {intake} patient {patient}")


@department_router.post("/{department}/intake_doctor")
async def update_intake_doctor(department: str, intakes: Dict[str, Intake] = Body(..., embed=True),
                               dal: MedicalDal = Depends(medical_dal)):
    for patient, intake in intakes.items():
        try:
            await dal.upsert_intake_doctor(patient, intake)
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} intake doctor - Patient not found', patient)
        except Exception as e:
            logger.exception(f"update intake failed - intake doctor {intake} patient {patient}")


@department_router.post("/{department}/discussion")
async def update_discussion(department: str, notes: Dict[str, Dict[str, Note]] = Body(..., embed=True),
                            dal: MedicalDal = Depends(medical_dal)):
    for patient, notes_by_id in notes.items():
        try:
            await dal.upsert_discussion(patient, notes_by_id)
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} discussion - Patient not found', patient)
        except Exception as e:
            logger.exception(f"update discussion failed - discussion {notes_by_id} patient {patient}")


@department_router.post("/{department}/destinations")
async def update_destinations(department: str, destinations: Dict[str, Optional[str]] = Body(..., embed=True),
                              dal: MedicalDal = Depends(medical_dal)):
    for record in destinations:
        try:
            await dal.upsert_destination(record, destinations[record])
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} destinations - Patient not found', record)
        except Exception as e:
            logger.exception(f"update destinations failed - record {record}")


@department_router.post("/{department}/doctors")
async def update_doctors(department: str, doctors: Dict[str, List[str]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for record in doctors:
        try:
            await dal.upsert_doctors(record, doctors[record])
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} doctors - Patient not found', record)
        except Exception as e:
            logger.exception(f"update doctors failed - record {record}")


@department_router.post("/{department}/medications")
async def update_medications(department: str, medications: Dict[str, List[Medication]] = Body(..., embed=True),
                             dal: MedicalDal = Depends(medical_dal)):
    for patient in medications:
        try:
            await dal.upsert_medications(patient, medications[patient])
        except PatientNotFoundException:
            logger.debug('Cannot update patient {} medications - Patient not found', patient)
