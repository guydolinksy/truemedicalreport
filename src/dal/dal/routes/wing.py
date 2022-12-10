import logbook
from fastapi import APIRouter, Depends
from common.data_models.bed import Bed
from common.data_models.wing import Wing
from ..clients import medical_dal
from ..dal.dal import MedicalDal

logger = logbook.Logger(__name__)
wing_router = APIRouter()


@wing_router.get("/{wing}", response_model=Wing, response_model_exclude_unset=True, tags=["Wing"])
def get_wing(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    return Wing(
        patients=dal.get_wing_patients(department, wing),
        details=dal.get_wing(department, wing),
        filters=dal.get_wing_filters(department, wing),
        notifications=dal.get_wing_notifications(department, wing)
    )


@wing_router.get("/{wing}/beds/{bed}", response_model=Bed, tags=["Wing"])
def get_patient_by_bed(department: str, wing: str, bed: str, dal: MedicalDal = Depends(medical_dal)) -> Bed:
    return Bed(patient=dal.get_patient_by_bed(department, wing, bed))
