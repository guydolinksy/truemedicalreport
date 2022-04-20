import logbook
from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every

from ..logics.sql_to_dal import SqlToDal
from ..logics.utils import inject_dependencies
from ..models.chameleon_main import Departments

updater_router = APIRouter()


def dal_updater() -> SqlToDal:
    return SqlToDal()


logger = logbook.Logger(__name__)


# TODO: uncomment to enable periodic updates
@updater_router.on_event('startup')
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admissions")
async def update_admissions(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    dal.update_admissions(department=department)


# TODO: uncomment to enable periodic updates
@updater_router.on_event('startup')
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements", status_code=201)
async def update_measurements(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    logger.info("Update measures...")
    dal.update_measurements(department=department)
    logger.info("Done.")
