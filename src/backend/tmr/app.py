from fastapi import FastAPI

from .wing import wing_router
from .patient import patient_router


def create_app() -> FastAPI:
    app_ = FastAPI(root_path='/api')
    app_.include_router(wing_router, prefix="/wing")
    app_.include_router(patient_router, prefix="/patient")
    return app_


app = create_app()
