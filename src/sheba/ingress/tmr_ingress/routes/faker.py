from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every
import logbook
from random import randint
from tmr_ingress.logics.faking import FakeMain
from tmr_ingress.logics.utils import inject_dependencies

faker_router = APIRouter()

logger = logbook.Logger(__name__)


# @faker_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@inject_dependencies()
@faker_router.post("/patients/admit", tags=["Patient"], status_code=201)
async def admit_patient(dal: FakeMain = Depends(FakeMain)):
    """
    fake new patient and add it to sql
    with 50% success chances
    :return:
    """
    logger.debug('Admitting patient...')
    await dal.admit_patients()
    logger.debug('Done.')


# @faker_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@inject_dependencies()
@faker_router.post("/patients/discharge", tags=["Patient"], status_code=201)
async def discharge_patient(dal: FakeMain = Depends(FakeMain)):
    """
    fake new patient and add it to sql
    with 50% success chances
    :return:
    """
    logger.debug('Discharging patient...')
    await dal.discharge_patient()
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=30, logger=logger)
@inject_dependencies()
@faker_router.post("/measurements", tags=["Measurements"], status_code=201)
async def generate_fake_measurements_for_all_patients(dal: FakeMain = Depends(FakeMain)):
    """
    generate fake measurements to all patients in SQL
    """
    logger.debug('Generating Fake Measurements for all patients...')
    await dal.update_measurements()
    logger.debug('Done.')
