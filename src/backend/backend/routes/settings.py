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


@settings_router.get('/department-items')
async def get_department_items(user_settings_=Depends(user_settings)):
    return getattr(user_settings_, 'department_items', [])


@settings_router.post('/department-items')
async def set_department_items(department_items, user_settings_=Depends(user_settings)):
    user_settings_.department_items = department_items
    return True
