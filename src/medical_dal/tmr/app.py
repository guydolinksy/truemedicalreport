import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler


def create_app() -> FastAPIOffline:
    app_ = FastAPIOffline(openapi_url='/medical-dal/openapi.json', docs_url='/medical-dal/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.websocket import websocket_router

    app_.include_router(patient_router, prefix="/medical-dal/patients")
    app_.include_router(department_router, prefix="/medical-dal/departments")
    app_.include_router(websocket_router, prefix="/medical-dal/sync")

    return app_


app = create_app()
