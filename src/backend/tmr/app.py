import sys

from fastapi import FastAPI

from tmr.routes.wing import wing_router
from tmr.routes.patient import patient_router
from tmr.routes.department import department_router
from tmr.routes.websocket import websocket_router

from logbook import StreamHandler


def create_app() -> FastAPI:
    app_ = FastAPI(openapi_url='/api/openapi.json', docs_url='/api/docs')
    app_.include_router(wing_router, prefix="/api/wings")
    app_.include_router(patient_router, prefix="/api/patients")
    app_.include_router(department_router, prefix="/api/departments")
    app_.include_router(websocket_router, prefix="/api/sync")

    StreamHandler(sys.stdout).push_application()

    return app_


app = create_app()
