from typing import Dict

import fastapi
from fastapi import Depends

from .auth import user_settings

settings_router = fastapi.APIRouter()


@settings_router.get('/display')
async def get_display_settings(user_settings_=Depends(user_settings)):
    return getattr(user_settings_, 'display', {})


@settings_router.post('/display')
async def set_display_settings(display: Dict, user_settings_=Depends(user_settings)):
    user_settings_.display = display
    return True
