from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.labs import LabTest, LabsResultsOfPatient
from tmr_common.data_models.measures import Measures, Measure
from tmr_common.data_models.patient import Patient, ExternalPatient
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.wing import WingOverview
from .wing import wing_router
from ..dal.dal import MedicalDal, Action

department_router = APIRouter()

department_router.include_router(wing_router, prefix="/{department}/wings")

logger = logbook.Logger(__name__)


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


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
        except ValueError:
            logger.exception('Cannot update measurements')


@department_router.post("/{department}/imaging")
async def update_imaging(department: str, images: Dict[str, List[Imaging]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for patient in {patient.external_id for patient in dal.get_department_patients(department)} | set(
            images):
        updated = {image.external_id: image for image in images.get(patient, [])}
        existing = {image.external_id: image for image in dal.get_patient_images(patient)}
        for image in set(existing) - set(updated):
            await dal.upsert_imaging(imaging_obj=existing[image], action=Action.remove)
        for image in set(updated) - set(existing):
            await dal.upsert_imaging(imaging_obj=updated[image], action=Action.insert)
        for image in set(updated) & set(existing):
            await dal.upsert_imaging(imaging_obj=updated[image], action=Action.update)


# TODO: Need to be tested
@department_router.post("/{department}/labs")
async def update_labs(department: str, labs: Dict[str, LabsResultsOfPatient] = Body(..., embed=True),
                      dal: MedicalDal = Depends(medical_dal)):
    for patient in {patient.external_id for patient in dal.get_department_patients(department)} | set(
            labs):
        updated = {lab_result.external_id: lab_result for lab_result in labs.get(patient, {})}
        existing = {lab_result.external_id: lab_result for lab_result in dal.get_patient_labs(patient)}
        for lab_result in set(existing) - set(updated):
            await dal.upsert_labs(labs_results=existing[lab_result], action=Action.remove)
        for lab_result in set(updated) - set(existing):
            await dal.upsert_labs(labs_results=existing[lab_result], action=Action.insert)
        for lab_result in set(updated) & set(existing):
            await dal.upsert_labs(labs_results=existing[lab_result], action=Action.update)
