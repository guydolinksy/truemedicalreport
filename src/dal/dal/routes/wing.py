import logbook
from fastapi import APIRouter, Depends

from common.data_models.bed import Bed
from common.data_models.wing import Wing
from common.utilities.exceptions import DepartmentNotFoundException, WingNotFoundException
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

logger = logbook.Logger(__name__)
wing_router = APIRouter()


@wing_router.get("/{wing}")
async def get_wing(department: str, wing: str, dal: MedicalDal = Depends(medical_dal)) -> Wing:
    async for d in dal.get_departments():
        if d.key == department:
            for w in d.wings:
                if w.details.key == wing:
                    return w
    else:
        raise WingNotFoundException


@wing_router.get("/{wing}/beds/{bed}")
async def get_patient_by_bed(department: str, wing: str, bed: str, dal: MedicalDal = Depends(medical_dal)) -> Bed:
    return await dal.get_bed(department, wing, bed)
