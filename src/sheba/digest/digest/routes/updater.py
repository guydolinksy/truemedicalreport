import datetime
import http

import logbook
from fastapi import APIRouter, Depends

from common.utilities.exceptions import safe, inject_dependencies
from common.wsp import register
from ..logics.sql_to_dal import SqlToDal, Departments

updater_router = APIRouter()


def dal_updater() -> SqlToDal:
    return SqlToDal()


logger = logbook.Logger(__name__)


@register(period=datetime.timedelta(seconds=40), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admissions")
def update_admissions(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update admissions...")
    res = dal.update_admissions(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=50), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements", status_code=201)
def update_measurements(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update measures...")
    res = dal.update_measurements(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=70), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_imagings", status_code=201)
def update_imagings(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update imagings...")
    res = dal.update_imaging(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_labs", status_code=201)
def update_labs(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update labs...")
    res = dal.update_labs(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_referrals", status_code=201)
def update_referrals(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update referrals...")
    res = dal.update_referrals(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=20), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_treatment")
def update_treatment(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Treatment...")
    res = dal.update_destination(department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/doctor_intake", status_code=http.HTTPStatus.ACCEPTED)
def update_doctor_intake(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Doctor Intake Info...")
    res = dal.update_doctor_intake(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/nurse_intake", status_code=http.HTTPStatus.ACCEPTED)
def update_nurse_intake(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Nurse Intake Info...")
    res = dal.update_nurse_intake(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=40), start_immediately=True)
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/medicines")
def update_medicines(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update medicines info...")
    res = dal.update_medicines(department=department)
    logger.debug("Done.")
    return res
