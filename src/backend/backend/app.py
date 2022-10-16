import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler


def create_app() -> FastAPIOffline:
    app_ = FastAPIOffline(openapi_url='/api/openapi.json', static_url="/api/static-offline-docs", docs_url='/api/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.auth import auth_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.websocket import websocket_router
    from .routes.settings import settings_router
    from .routes.warnings import subscriber_router

    app_.include_router(auth_router, prefix="/api/auth")
    app_.include_router(patient_router, prefix="/api/patients")
    app_.include_router(department_router, prefix="/api/departments")
    app_.include_router(websocket_router, prefix="/api/sync")
    app_.include_router(settings_router, prefix="/api/settings")
    app_.include_router(subscriber_router, prefix="/api/subscribe")

    return app_


app = create_app()
