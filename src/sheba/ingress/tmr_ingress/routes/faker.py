from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every
import logbook
from random import randint
from tmr_ingress.logics.faking import FakeMain
from tmr_ingress.logics.utils import inject_dependencies
from tmr_ingress.models.chameleon_main import Departments

faker_router = APIRouter()

logger = logbook.Logger(__name__)


@faker_router.on_event('startup')
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/patients/admit", tags=["Patient"], status_code=201)
async def admit_patient(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    fake new patient and add it to sql
    with 50% success chances
    :return:
    """
    logger.debug('Admitting patient...')
    await dal.admit_patients(department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=20, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/patients/discharge", tags=["Patient"], status_code=201)
async def discharge_patient(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    fake new patient and add it to sql
    with 50% success chances
    :return:
    """
    logger.debug('Discharging patient...')
    await dal.discharge_patient(department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=20, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/measurements", tags=["Measurements"], status_code=201)
async def generate_fake_measurements_for_all_patients(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake measurements to all patients in SQL
    """
    logger.debug('Generating Fake Measurements for all patients...')
    await dal.update_measurements(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=180, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/imagings", tags=["Imagings"], status_code=201)
async def generate_imagings(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating Fake Imagings for all patients...')
    await dal.update_imagings(department=department)
    logger.debug('Done.')
