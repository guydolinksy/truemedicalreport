import logbook
from fastapi import APIRouter, Depends

from common.data_models.bed import Bed
from common.data_models.wing import Wing
from common.utilities.exceptions import DepartmentNotFoundException, WingNotFoundException
from ..clients import medical_dal
from ..dal.medical_dal import MedicalDal

logger = logbook.Logger(__name__)
wing_router = APIRouter()
