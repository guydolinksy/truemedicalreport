import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler
from common.tracing import setup_sentry
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from . import config


def create_app() -> FastAPIOffline:
    if config.sentry_dsn:
        setup_sentry(config.sentry_dsn, extra_integrations=[
            SqlalchemyIntegration()
        ])

    app_ = FastAPIOffline(openapi_url='/digest/openapi.json', static_url="/digest/static-offline-docs",
                          docs_url='/digest/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.updater import updater_router
    app_.include_router(updater_router, prefix="/digest")

    from common.wsp import router as scheduler_router
    app_.include_router(scheduler_router, prefix="/digest/scheduler")

    from .logics.startup import startup
    app_.on_event('startup')(startup)

    return app_


app = create_app()
