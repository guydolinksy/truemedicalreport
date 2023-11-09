from typing import List

from fastapi import APIRouter, Depends, Body

from common.data_models.mci import MCIResult
from dal.clients import application_dal, medical_dal
from dal.dal.medical_dal import MedicalDal
from dal.dal.application_dal import ApplicationDal
from common.data_models.patient import Patient

mci_router = APIRouter()


@mci_router.get('/form')
async def get_form_options(dal: ApplicationDal = Depends(application_dal)):
    return (await dal.get_config('mci_form', []))['value']


@mci_router.post('/patient')
async def create_anonymous_patient(patient: Patient = Body(..., embed=True), dal: MedicalDal = Depends(medical_dal)):
    return await dal.insert_patient(patient)


@mci_router.post('/merge')
async def merge_anonymous_with_real_patient(anonymous: str = Body(..., embed=True),
                                            patient: str = Body(..., embed=True),
                                            dal: MedicalDal = Depends(medical_dal)):
    await dal.merge_mci_patient(anonymous, patient)


@mci_router.post('/unmerge')
async def unmerge_patients(patient_id: str = Body(..., embed=True), dal: MedicalDal = Depends(medical_dal)):
    await dal.unmerge_mci_patient(patient_id)

@mci_router.post('/mci_to_mongo')
async def mci_to_db(results: List[MCIResult] = Body(..., embed=True), id_: str = Body(..., embed=True),
                    dal: MedicalDal = Depends(medical_dal)):
    await dal.update_mci(results=results, id_=id_)
