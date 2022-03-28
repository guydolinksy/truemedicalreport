from fastapi import FastAPI

from tmr.routes.wing import wing_router
from tmr.routes.patient import patient_router
from tmr.routes.department import department_router


def create_app() -> FastAPI:
    app_ = FastAPI(root_path='/api')
    app_.include_router(wing_router, prefix="/wing")
    app_.include_router(patient_router, prefix="/patient")
    app_.include_router(department_router, prefix="/department")

    return app_


app = create_app()
