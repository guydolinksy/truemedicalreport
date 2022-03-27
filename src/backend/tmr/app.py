from fastapi import FastAPI

from .wing import wing_router


def create_app() -> FastAPI:
    app_ = FastAPI(root_path='/api')
    app_.include_router(wing_router, prefix="/wing")
    return app_


app = create_app()
