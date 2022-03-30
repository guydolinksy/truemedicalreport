from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from ..dal.dal import MedicalDal

patient_router = APIRouter()


# TODO remove duplicate use of medical_dal function
def medical_dal() -> MedicalDal:
    return MedicalDal(MongoClient("medical-db").tmr)


@patient_router.get("/bed/{bed}")
def get_patient_info_by_id(bed: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.get_patient_info_by_bed(bed)


@patient_router.get("/id/{patient_id}")
def get_patient_info_by_id(patient_id: str, dal: MedicalDal = Depends(medical_dal)) -> dict:
    return dal.get_patient_info_by_id(patient_id)


@patient_router.post("/id/{patient_id}")
def update_patient_info_by_id(patient_id: str, path=Body(...), value=Body(...), data=Body(...),
                              dal: MedicalDal = Depends(medical_dal)) -> bool:
    return dal.update_patient_info_by_id(patient_id, path, value, data)


@patient_router.post("/id/{patient_id}/warning")
async def warn_patient_by_id(patient_id: str, warning=Body(...), dal: MedicalDal = Depends(medical_dal)) -> bool:
    update_result = dal.append_warning_to_patient_by_id(patient_id, warning)
    if not update_result:
        return update_result

    await notify(patient_id)  # Todo: is this correct?
    return True
