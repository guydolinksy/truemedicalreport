import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler
from sentry_sdk.integrations.pymongo import PyMongoIntegration

from common.tracing import setup_sentry

from .consts import DAL_FAKER_TAG_NAME
from . import config

def create_app() -> FastAPIOffline:
    if config.sentry_dsn:
        setup_sentry(config.sentry_dsn, extra_integrations=[
            # Even though we use Motor, the async MongoDB client, it uses PyMongo under the hood -
            # meaning, it'll be correctly traced.
            PyMongoIntegration()
        ])

    app_ = FastAPIOffline(
        openapi_url="/dal/openapi.json",
        static_url="/dal/static-offline-docs",
        docs_url="/dal/docs",
        openapi_tags=[
            {
                "name": DAL_FAKER_TAG_NAME,
                "description": "Fakes things on the DAL level (no need for digest)"
            }
        ]
    )

    StreamHandler(sys.stdout).push_application()

    from .routes.init import init_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.publishing import publish_router
    from .routes.faking import faker_router

    app_.include_router(init_router, prefix="/dal/init")
    app_.include_router(patient_router, prefix="/dal/patients")
    app_.include_router(department_router, prefix="/dal/departments")
    app_.include_router(publish_router, prefix="/dal/publishing")
    app_.include_router(faker_router, prefix="/dal/faker")

    return app_


app = create_app()
