from typing import Dict

import fastapi

from .. import config

tracing_router = fastapi.APIRouter()


@tracing_router.get('/dsn')
async def get_dsn() -> str:
    return config.sentry_dsn
