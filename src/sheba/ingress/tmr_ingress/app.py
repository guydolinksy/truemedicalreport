import sys

from fastapi import FastAPI
from logbook import StreamHandler


def create_app() -> FastAPI:
    app_ = FastAPI(openapi_url='/ingress/openapi.json', docs_url='/ingress/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.updater import updater_router
    app_.include_router(updater_router, prefix="/ingress")

    from .logics.startup import startup
    app_.on_event('startup')(startup)

    return app_


app = create_app()
