from typing import Dict

import fastapi
from fastapi import Depends

from .auth import manager
from ..logics.settings import user_settings

settings_router = fastapi.APIRouter()


@settings_router.get('/display')
async def patient_handler(user=Depends(manager)):
    return (user_settings.find_one({'user': user['username']}, {'display': 1}) or {}).get('display', {})


@settings_router.post('/display')
async def patient_handler(display: Dict, user=Depends(manager)):
    user_settings.update_one({'user': user['username']}, {'$set': {'display': display}}, upsert=True)
    return True
