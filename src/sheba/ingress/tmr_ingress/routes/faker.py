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
@repeat_every(seconds=60, logger=logger)
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
@repeat_every(seconds=240, logger=logger)
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
@repeat_every(seconds=30, logger=logger)
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
@repeat_every(seconds=60, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/imagings", tags=["Imagings"], status_code=201)
async def generate_imagings(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating Fake Imagings for all patients...')
    await dal.update_imagings(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=45, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/labs", tags=["Labs"], status_code=201)
async def generate_labs(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating Fake Labs for all patients...')
    await dal.update_labs(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=90, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/referrals", tags=["referrals"], status_code=201)
async def generate_referrals(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating Fake Referrals for all patients...')
    await dal.update_referrals(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=3600, wait_first=True, logger=logger)
@inject_dependencies()
@faker_router.post("/clear", status_code=201)
async def clear(dal: FakeMain = Depends(FakeMain)):
    logger.info("Clearing...")
    dal.clear()
    logger.info("Done.")


@faker_router.on_event('startup')
@repeat_every(seconds=60, wait_first=True, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/nurse_summarize", status_code=201)
async def generate_nurse_summarize(department: Departments, dal: FakeMain = Depends(FakeMain)):
    logger.info("Generate Nurse Summarize")
    await dal.add_nurse_medical_text_to_department(department=department)
    logger.info("Done Generate Nurse Summarize")
