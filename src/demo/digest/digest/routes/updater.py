import http
from enum import Enum

import logbook
from fastapi import APIRouter

from common.utilities.exceptions import inject_dependencies, safe

updater_router = APIRouter()

logger = logbook.Logger(__name__)


class Departments(int, Enum):
    er = '1184000'


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admissions")
async def update_admissions(department: Departments):
    logger.debug("Update admissions...")
    res = dal.update_admissions(department=department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements", status_code=201)
async def update_measurements(department: Departments):
    logger.debug("Update measures...")
    res = dal.update_measurements(department=department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_imagings", status_code=201)
async def update_imagings(department: Departments):
    logger.debug("Update imagings...")
    res = dal.update_imaging(department=department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_labs", status_code=201)
async def update_labs(department: Departments):
    logger.debug("Update labs...")
    res = dal.update_labs(department=department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_referrals", status_code=201)
async def update_referrals(department: Departments):
    logger.debug("Update referrals...")
    res = dal.update_referrals(department=department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_treatment")
async def update_treatment(department: Departments):
    logger.debug("Update Treatment...")
    res = dal.update_destination(department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/doctor_intake", status_code=http.HTTPStatus.ACCEPTED)
async def update_doctor_intake(department: Departments):
    logger.debug("Update Doctor Intake Info...")
    res = dal.update_doctor_intake(department=department)
    logger.debug("Done.")
    return res


@updater_router.on_event('startup')
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/nurse_intake", status_code=http.HTTPStatus.ACCEPTED)
async def update_nurse_intake(department: Departments):
    logger.debug("Update Nurse Intake Info...")
    res = dal.update_nurse_intake(department=department)
    logger.debug("Done.")
    return res


@updater_router.post("/medications")
async def update_medications(department: Departments):
    logger.debug("Update medications info...")
    res = dal.update_medications(department=department)
    logger.debug("Done.")
    return res
