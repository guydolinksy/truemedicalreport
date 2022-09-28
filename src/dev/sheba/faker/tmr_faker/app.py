import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler


def create_app() -> FastAPIOffline:
    app_ = FastAPIOffline(openapi_url='/faker/openapi.json', static_url="/faker/static-offline-docs", docs_url='/faker/docs')

    StreamHandler(sys.stdout).push_application()

    from .routes.faker import faker_router
    app_.include_router(faker_router, prefix="/faker")

    return app_


app = create_app()
