import sys

from fastapi import FastAPI

from tmr.routes.wing import wing_router
from tmr.routes.patient import patient_router
from tmr.routes.department import department_router
from tmr.routes.websocket import websocket_router

from logbook import StreamHandler


def create_app() -> FastAPI:
    app_ = FastAPI(root_path='/api')
    app_.include_router(wing_router, prefix="/wings")
    app_.include_router(patient_router, prefix="/patients")
    app_.include_router(department_router, prefix="/departments")
    app_.include_router(websocket_router)

    StreamHandler(sys.stdout).push_application()

    return app_


app = create_app()
