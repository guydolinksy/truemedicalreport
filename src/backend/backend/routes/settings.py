from typing import Dict

import fastapi
from fastapi import Depends, Body

from .auth import user_settings

settings_router = fastapi.APIRouter()


@settings_router.get('/view/{view}/mode/{mode}/info/format')
async def get_display_settings(
        view: str, mode: str,
        user_settings_=Depends(user_settings)
):
    return {
        'components': [
            dict(
                type='MCISection',
                name='מנגנון פציעה',
                config=dict(
                    style=dict(
                        flex=1
                    ),
                    options=[dict(
                        key="gunshot",
                        name="פצע ירי",
                        customizers=[dict(
                            key='location',
                            name='מיקום',
                            type='location',
                        )]
                    )]
                ),
            ),
            dict(
                type='MCISection',
                name='טיפול בשטח',
                config=dict(
                    style=dict(
                        flex=1
                    ),
                    options=[dict(
                        key="drug",
                        name="תרופה",
                        customizers=[dict(
                            key='name',
                            name='סוג התרופה',
                            type='select',
                            options=['אדרנלין', 'דורמיקום']
                        ), dict(
                            key='dosage',
                            name='מינון',
                            type='select',
                            options=['0.5mg', '1mg']
                        )]
                    )]
                ),
            ),
        ]
    }


@settings_router.get('/display')
async def get_display_settings(user_settings_=Depends(user_settings)):
    return getattr(user_settings_, 'display', {})


@settings_router.post('/display')
async def set_display_settings(display: Dict, user_settings_=Depends(user_settings)):
    user_settings_.display = display
    return True


@settings_router.post('/statistics')
async def set_department_items(statistics: dict = Body(..., embed=True), user_settings_=Depends(user_settings)):
    user_settings_.statistics = statistics
    return True
