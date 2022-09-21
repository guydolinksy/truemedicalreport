import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler


def create_app() -> FastAPIOffline:
    app_ = FastAPIOffline(openapi_url='/dal/openapi.json', docs_url='/dal/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.init import init_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.websocket import websocket_router

    app_.include_router(init_router, prefix="/dal/init")
    app_.include_router(patient_router, prefix="/dal/patients")
    app_.include_router(department_router, prefix="/dal/departments")
    app_.include_router(websocket_router, prefix="/dal/sync")

    return app_


app = create_app()
