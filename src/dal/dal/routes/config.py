import logbook
from fastapi import APIRouter, Depends, Body

from ..clients import application_dal
from ..dal.application_dal import ApplicationDal

config_router = APIRouter()

logger = logbook.Logger(__name__)


@config_router.post("/set")
async def set_config(key: str = Body(..., embed=True), version: str = Body(..., embed=True),
                     value=Body(..., embed=True), dal: ApplicationDal = Depends(application_dal)):
    return await dal.set_config(key=key, version=version, value=value)

@config_router.post("/get")
async def get_config(key: str = Body(..., embed=True), default=Body(..., embed=True),
                     dal: ApplicationDal = Depends(application_dal)):
    return await dal.get_config(key=key, default=default)
