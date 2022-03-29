from fastapi import FastAPI

from .routes.wing import wing_router
from .routes.patient import patient_router
from .routes.department import department_router
from .routes.websocket import websocket_router


def create_app() -> FastAPI:
    app_ = FastAPI()
    app_.include_router(wing_router, prefix="/medical_dal/wing")
    app_.include_router(patient_router, prefix="/medical_dal/patient")
    app_.include_router(department_router, prefix="/medical_dal/department")
    app_.include_router(websocket_router)

    return app_


app = create_app()
