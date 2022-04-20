from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every
import logbook
from random import randint
from ..faker.fake_data.fake_main import FakeMain

faker_router = APIRouter()

logger = logbook.Logger(__name__)


@faker_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@faker_router.post("/patient", tags=["Patient"], status_code=201)
def generate_fake_patient():
    """
    fake new patient and add it to sql
    with 50% success chances
    """
    logger.debug('Generating patient...')

    if randint(0, 1):
        FakeMain().insert_new_patient()

    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=30, logger=logger)
@faker_router.post("/measurement", tags=["Measurements"], status_code=201)
def generate_fake_measurements_for_all_patients():
    """
    generate fake measurements  to all patients in SQL
    """
    logger.debug('Generating Fake Measurements for all patients...')
    FakeMain().insert_new_measurements()
    logger.debug('Done.')
