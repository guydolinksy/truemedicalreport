import logbook
from fastapi import APIRouter, Depends
from common.data_models.bed import Bed
from common.data_models.wing import Wing
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

logger = logbook.Logger(__name__)
wing_router = APIRouter()


@wing_router.get("/{wing}", response_model=Wing, response_model_exclude_unset=True, tags=["Wing"])
async def get_wing(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    return Wing(
        patients=await dal.get_wing_patients(department, wing),
        details=await dal.get_wing_details(department, wing),
        filters=await dal.get_wing_filters(department, wing),
        notifications=await dal.get_wing_notifications(department, wing)
    )


@wing_router.get("/{wing}/beds/{bed}", response_model=Bed, tags=["Wing"])
async def get_patient_by_bed(department: str, wing: str, bed: str, dal: MedicalDal = Depends(medical_dal)) -> Bed:
    patient = await dal.get_patient_by_bed(department, wing, bed)
    return Bed(patient=patient)
