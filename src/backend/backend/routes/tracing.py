import fastapi

from .. import config

tracing_router = fastapi.APIRouter()


@tracing_router.get('/config')
async def get_matomo():
    return {"sentryDsn": config.sentry_dsn, "matomoUrlBase": config.matomo_url, "matomoSiteId": config.matomo_site_id}
