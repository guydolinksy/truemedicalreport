from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from tmr_common.data_models.measures import Measures
from tmr_common.data_models.patient import Patient
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.wing import WingOverview
from .patient import upsert_patient, upsert_image
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
async def update_admissions(department: str, admissions: List[Patient] = Body(..., embed=True),
                            dal: MedicalDal = Depends(medical_dal)):
    updated = {patient.chameleon_id: patient for patient in admissions}
    existing = {patient.chameleon_id: patient for patient in dal.get_department_patients(department)}
    for patient in set(existing) - set(updated):
        await upsert_patient(patient=existing[patient], dal=dal, action=Action.remove)
    for patient in set(updated) - set(existing):
        await upsert_patient(patient=updated[patient], dal=dal, action=Action.insert)
    for patient in set(updated) & set(existing):
        await upsert_patient(patient=updated[patient], dal=dal, action=Action.update)


@department_router.post("/{department}/measurements", tags=["Department"])
async def update_measurements(measurements: Dict[str, Measures] = Body(..., embed=True),
                              dal: MedicalDal = Depends(medical_dal)):
    for patient in measurements:
        await dal.upsert_measurements(patient, measurements[patient])


@department_router.post("/{department}/imaging")
async def update_imaging(department: str, images: Dict[str, List[Imaging]] = Body(..., embed=True),
                         dal: MedicalDal = Depends(medical_dal)):
    for patient in {patient.chameleon_id for patient in dal.get_department_patients(department)} | set(images):
        updated = {image.chameleon_id: image for image in images.get(patient,[])}
        existing = {image.chameleon_id: image for image in dal.get_patient_images(patient)}
        for image in set(existing) - set(updated):
            await upsert_image(image=existing[image], dal=dal, action=Action.remove)
        for image in set(updated) - set(existing):
            await upsert_image(image=updated[image], dal=dal, action=Action.insert)
        for image in set(updated) & set(existing):
            await upsert_image(image=updated[image], dal=dal, action=Action.update)
