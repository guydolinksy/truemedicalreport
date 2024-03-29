import asyncio
import datetime
import http
from typing import List

import logbook
from fastapi import APIRouter, Depends, Body

from common.data_models.mci import MCIResult
from common.utilities.exceptions import safe, inject_dependencies
from common.wsp import register
from ..logics.sql_to_dal import SqlToDal, Departments
from .mci import mci_data

updater_router = APIRouter()


def dal_updater() -> SqlToDal:
    return SqlToDal()


logger = logbook.Logger(__name__)


@register(period=datetime.timedelta(seconds=40))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admissions")
def update_admissions(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update admissions...")
    res = dal.update_admissions(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=50))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements", status_code=201)
def update_measurements(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update measures...")
    res = dal.update_measurements(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=70))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_imagings", status_code=201)
def update_imagings(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update imagings...")
    res = dal.update_imaging(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_labs", status_code=201)
def update_labs(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update labs...")
    res = dal.update_labs(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_referrals", status_code=201)
def update_referrals(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update referrals...")
    res = dal.update_referrals(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=20))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_destinations")
def update_destinations(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Destinations...")
    res = dal.update_destination(department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/doctor_notes", status_code=http.HTTPStatus.ACCEPTED)
def update_doctor_notes(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Doctor Notes...")
    res = dal.update_doctor_notes(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/doctor_intake", status_code=http.HTTPStatus.ACCEPTED)
def update_doctor_intake(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Doctor Intake Info...")
    res = dal.update_doctor_intake(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=60))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/nurse_intake", status_code=http.HTTPStatus.ACCEPTED)
def update_nurse_intake(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update Nurse Intake Info...")
    res = dal.update_nurse_intake(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=40))
@safe(logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/medications")
def update_medications(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.debug("Update medications info...")
    res = dal.update_medications(department=department)
    logger.debug("Done.")
    return res


@register(period=datetime.timedelta(seconds=1000))
@safe(logger)
@inject_dependencies(safety_buffer=120)
@updater_router.post("/update_chameleon", status_code=201)
def update_chameleon(safety_buffer: int = Body(..., embed=True)):
    asyncio.run(mci_data(safety_buffer))
    logger.debug("Update chameleon mci...")


@updater_router.get('/update_chameleon_check', status_code=201)
async def update_chameleon_check() -> List[MCIResult]:
    return await mci_data(10)
