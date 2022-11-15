import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler


def create_app() -> FastAPIOffline:
    app_ = FastAPIOffline(openapi_url='/digest/openapi.json', static_url="/digest/static-offline-docs", docs_url='/digest/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.updater import updater_router
    app_.include_router(updater_router, prefix="/digest")

    from .logics.startup import startup
    app_.on_event('startup')(startup)

    return app_


app = create_app()
