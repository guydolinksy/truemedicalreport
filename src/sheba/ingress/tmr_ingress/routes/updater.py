import http

import logbook
from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every

from ..logics.sql_to_dal import SqlToDal
from ..logics.utils import inject_dependencies, safe
from ..models.chameleon_main import Departments

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
    logger.info("Update admissions...")
    dal.update_admissions(department=department)
    logger.info("Done.")


# TODO: uncomment to enable periodic updates
@updater_router.on_event('startup')
@repeat_every(seconds=50, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements", status_code=201)
async def update_measurements(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.info("Update measures...")
    dal.update_measurements(department=department)
    logger.info("Done.")


# TODO: uncomment to enable periodic updates
@updater_router.on_event('startup')
@repeat_every(seconds=70, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_imagings", status_code=201)
async def update_imagings(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.info("Update imagings...")
    dal.update_imaging(department=department)
    logger.info("Done.")


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_labs", status_code=201)
async def update_labs(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.info("Update labs...")
    dal.update_labs(department=department)
    logger.info("Done.")


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_referrals", status_code=201)
async def update_referrals(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.info("Update referrals...")
    dal.update_referrals(department=department)
    logger.info("Done.")


@updater_router.on_event('startup')
@safe(logger)
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admission_treatment_decision/")
async def update_admission_treatment_decision(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Treatment")
    dal.update_admission_treatment_decision(department)


@updater_router.on_event('startup')
@repeat_every(seconds=60, logger=logger)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/nurse_summary", status_code=http.HTTPStatus.ACCEPTED)
async def update_basic_medical(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.info("Update Basic Medical Info...")
    dal.update_basic_medical(department=department)
    logger.info("Done.")

