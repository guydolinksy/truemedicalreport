from fastapi import APIRouter, Depends

from dal.clients import application_dal
from dal.dal.application_dal import ApplicationDal

mci_router = APIRouter()


@mci_router.get('/form')
async def get_form_options(dal: ApplicationDal = Depends(application_dal)):
    return (await dal.get_config('mci_form', []))['value']
