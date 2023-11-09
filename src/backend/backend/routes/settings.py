from typing import Dict

import fastapi
from fastapi import Depends, Body

from .auth import user_settings

settings_router = fastapi.APIRouter()


@settings_router.get('/views/{view_type}/{view}/modes/{mode}/info/format')
async def get_display_settings(
        view_type: str,
        view: str,
        mode: str,
        user_settings_=Depends(user_settings)
):
    return {
        'components': [
            dict(
                key='header',
                type='MCIHeader',
                config=dict(
                    key='header',
                    customStyle=dict(
                        gridColumn='1 / -1',
                    ),
                    sections=[
                        dict(
                            key='occupation',
                            options=[
                                dict(
                                    key="soldier",
                                    name="חייל",
                                ), dict(
                                    key="civilian",
                                    name="אזרח",
                                ),
                            ],
                        ),
                        dict(
                            key='transportation',
                            options=[
                                dict(
                                    key="by-air",
                                    name="מסוק",
                                ), dict(
                                    key="by-land",
                                    name="אמבולנס",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            dict(
                key='diagnosis',
                type='MCISection',
                name='מנגנון פציעה',
                config=dict(
                    key='diagnosis',
                    name='מנגנון פציעה',
                    customStyle=dict(
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
                    ), dict(
                        key="stab_wound",
                        name="פצע דקירה",
                        customizers=[dict(
                            key='location',
                            name='מיקום',
                            type='location',
                        )]
                    )]
                ),
            ),
            dict(
                key='pre_hospital_treatment',
                type='MCISection',
                name='טיפול בשטח',
                config=dict(
                    key='pre_hospital_treatment',
                    name='טיפול בשטח',
                    customStyle=dict(
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
            dict(
                key='hospital_treatment',
                type='MCISection',
                name='טיפול בבית החולים',
                config=dict(
                    key='hospital_treatment',
                    name='טיפול בבית החולים',
                    customStyle=dict(
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
            dict(
                key='imaging',
                type='MCISection',
                name='הדמיה',
                config=dict(
                    key='imaging',
                    name='הדמיה',
                    customStyle=dict(
                        flex=1
                    ),
                    options=[dict(
                        key="mri",
                        name="MRI",
                        customizers=[dict(
                            key='location',
                            name='מיקום',
                            type='location'
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
