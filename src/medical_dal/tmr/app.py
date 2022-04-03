import sys

from fastapi import FastAPI
from logbook import StreamHandler


def create_app() -> FastAPI:
    app_ = FastAPI(openapi_url='/medical_dal/openapi.json', docs_url='/medical_dal/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.wing import wing_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.websocket import websocket_router

    app_.include_router(wing_router, prefix="/medical_dal/wing")
    app_.include_router(patient_router, prefix="/medical_dal/patient")
    app_.include_router(department_router, prefix="/medical_dal/department")
    app_.include_router(websocket_router, prefix="/medical_dal/sync")

    return app_


app = create_app()
