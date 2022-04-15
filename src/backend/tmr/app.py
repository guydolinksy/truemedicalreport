import sys

from fastapi import FastAPI
from logbook import StreamHandler


def create_app() -> FastAPI:
    app_ = FastAPI(openapi_url='/api/openapi.json', docs_url='/api/docs')

    StreamHandler(sys.stdout).push_application()

    from .logics.auth import auth_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.websocket import websocket_router
    from .logics.warnings import subscriber_router

    app_.include_router(auth_router, prefix="/api/auth")
    app_.include_router(patient_router, prefix="/api/patients")
    app_.include_router(department_router, prefix="/api/departments")
    app_.include_router(websocket_router, prefix="/api/sync")
    app_.include_router(subscriber_router)

    return app_


app = create_app()
