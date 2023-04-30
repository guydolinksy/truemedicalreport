import logbook
from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every
import http
from tmr_faker.logics.faking import FakeMain, Departments
from common.utilities.exceptions import inject_dependencies

faker_router = APIRouter()

logger = logbook.Logger(__name__)


@faker_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/patients/admit", tags=["Patient"], status_code=201)
def admit_patient(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    fake new patient and add it to sql
    with 50% success chances
    :return:
    """
    logger.debug('Admitting patient...')
    dal.admit_patients(department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=240, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/patients/discharge", tags=["Patient"], status_code=http.HTTPStatus.OK)
def discharge_patient(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    fake new patient and add it to sql
    with 50% success chances
    :return:
    """
    logger.debug('Discharging patient...')
    dal.discharge_patient(department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=120, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/measurements", tags=["Measurements"], status_code=201)
def generate_measurements(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake measurements to all patients in SQL
    """
    logger.debug('Generating fake measurements for all patients...')
    dal.update_measurements(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=300, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/imagings", tags=["Imagings"], status_code=201)
def generate_imagings(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating fake imagings for all patients...')
    dal.update_imagings(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=300, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/labs", tags=["Labs"], status_code=201)
def generate_labs(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating demo labs for all patients...')
    dal.update_labs(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=300, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/referrals", tags=["referrals"], status_code=201)
def generate_referrals(department: Departments, dal: FakeMain = Depends(FakeMain)):
    """
    generate fake imagings to all patients in SQL
    """
    logger.debug('Generating demo referrals for all patients...')
    dal.update_referrals(department=department)
    logger.debug('Done.')


@faker_router.on_event('startup')
@repeat_every(seconds=120, wait_first=True, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/nurse_summaries", status_code=201)
def generate_nurse_summaries(department: Departments, dal: FakeMain = Depends(FakeMain)):
    logger.info("Generate demo nurse summary...")
    dal.update_nurse_summaries(department=department)
    logger.info("Done.")


@faker_router.on_event('startup')
@repeat_every(seconds=240, wait_first=True, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/doctor_visits", status_code=201)
def generate_doctor_visits(department: Departments, dal: FakeMain = Depends(FakeMain)):
    logger.info("Generate demo doctor visits...")
    dal.update_doctor_visits(department=department)
    logger.info("Done.")


@faker_router.on_event('startup')
@repeat_every(seconds=60, wait_first=True, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/room_placements", status_code=201)
def generate_room_placements(department: Departments, dal: FakeMain = Depends(FakeMain)):
    logger.info("Generate room placements...")
    dal.update_room_placements(department=department)
    logger.info("Done generate room placements")


@faker_router.on_event('startup')
@repeat_every(seconds=600, wait_first=True, logger=logger)
@inject_dependencies(department=Departments.er)
@faker_router.post("/treatments", status_code=201)
def generate_treatments(department: Departments, dal: FakeMain = Depends(FakeMain)):
    logger.info("Generate treatment...")
    dal.update_treatment(department=department)
    logger.info("Done generate treatment")


@faker_router.on_event('startup')
@repeat_every(seconds=3600, wait_first=True, logger=logger)
@inject_dependencies()
@faker_router.post("/clear", status_code=201)
def clear(dal: FakeMain = Depends(FakeMain)):
    logger.info("Clearing...")
    dal.clear()
    logger.info("Done.")
