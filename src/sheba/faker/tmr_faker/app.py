import sys

from fastapi import FastAPI
from logbook import StreamHandler


def create_app() -> FastAPI:
    app_ = FastAPI(openapi_url='/faker/openapi.json', docs_url='/faker/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.faker import faker_router
    app_.include_router(faker_router, prefix="/faker")

    return app_


app = create_app()
