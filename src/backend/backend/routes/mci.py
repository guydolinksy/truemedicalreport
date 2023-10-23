from fastapi import APIRouter, Depends

from backend.logics.utils import fetch_dal_json

mci_router = APIRouter()


@mci_router.get('/form')
async def get_form_options():
    return await fetch_dal_json("/mci/form")
