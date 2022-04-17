import logbook
from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every

from ..logics.sql_to_dal import SqlToDal, Departments
from ..logics.utils import inject_dependencies

updater_router = APIRouter()


def dal_updater() -> SqlToDal:
    return SqlToDal()


logger = logbook.Logger(__name__)


# TODO: uncomment to enable periodic updates
# @updater_router.on_event('startup')
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_admissions")
async def update_admissions(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    dal.update_admissions(department=department)


# TODO: uncomment to enable periodic updates
# @updater_router.on_event('startup')
@repeat_every(seconds=10, logger=logger)
@inject_dependencies(department=Departments.er)
@updater_router.post("/update_measurements")
async def update_measurements(department: Departments, dal: SqlToDal = Depends(dal_updater)):
    dal.update_measurements(department=department)
