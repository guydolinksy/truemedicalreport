import http

import logbook
from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every

from ..logics.sql_to_dal import SqlToDal, Departments
from ..logics.utils import inject_dependencies, safe

updater_router = APIRouter()


def dal_updater() -> SqlToDal:
    return SqlToDal()


logger = logbook.Logger(__name__)


@updater_router.on_event('startup')
@repeat_every(seconds=40, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admissions")
async def update_admissions(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update admissions...")
    res = dal.update_admissions(department=department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@repeat_every(seconds=50, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements", status_code=201)
async def update_measurements(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update measures...")
    res = dal.update_measurements(department=department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@repeat_every(seconds=70, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_imagings", status_code=201)
async def update_imagings(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update imagings...")
    res = dal.update_imaging(department=department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_labs", status_code=201)
async def update_labs(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update labs...")
    res = dal.update_labs(department=department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_referrals", status_code=201)
async def update_referrals(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update referrals...")
    res = dal.update_referrals(department=department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@safe(logger)
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_treatment")
async def update_treatment(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Treatment...")
    res = dal.update_destination(department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/doctor_intake", status_code=http.HTTPStatus.ACCEPTED)
async def update_doctor_intake(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Doctor Intake Info...")
    res = dal.update_doctor_intake(department=department)
    logger.debug("Done.")
    # return res


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/nurse_intake", status_code=http.HTTPStatus.ACCEPTED)
async def update_nurse_intake(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Nurse Intake Info...")
    res = dal.update_nurse_intake(department=department)
    logger.debug("Done.")
    # return res


@updater_router.post("/medicines")
async def update_medicines(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update medicines info...")
    res = dal.update_medicines()
    logger.debug("Done.")
    # return res
