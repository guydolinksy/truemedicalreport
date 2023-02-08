import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler

from common.tracing import setup_sentry

from . import config


def create_app() -> FastAPIOffline:
    if config.sentry_dsn:
        setup_sentry(config.sentry_dsn)

    app_ = FastAPIOffline(openapi_url='/api/openapi.json', static_url="/api/static-offline-docs", docs_url='/api/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.auth import auth_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.sync import sync_router
    from .routes.settings import settings_router
    from .routes.tracing import tracing_router

    app_.include_router(auth_router, prefix="/api/auth")
    app_.include_router(patient_router, prefix="/api/patients")
    app_.include_router(department_router, prefix="/api/departments")
    app_.include_router(sync_router, prefix="/api/sync")
    app_.include_router(settings_router, prefix="/api/settings")
    app_.include_router(tracing_router, prefix="/api/tracing")

    return app_


app = create_app()
