import sys

from fastapi_offline import FastAPIOffline
from logbook import StreamHandler
from sentry_sdk.integrations.pymongo import PyMongoIntegration

from common.tracing import setup_sentry
from . import config
from .consts import DAL_FAKER_TAG_NAME


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

    from .routes.config import config_router
    from .routes.patient import patient_router
    from .routes.department import department_router
    from .routes.mci import mci_router
    from .routes.publishing import publish_router
    from .routes.faking import faker_router
    from .routes.gql_example import gql_router

    app_.include_router(config_router, prefix="/dal/config")
    app_.include_router(patient_router, prefix="/dal/patients")
    app_.include_router(department_router, prefix="/dal/departments")
    app_.include_router(mci_router, prefix="/dal/mci")
    app_.include_router(publish_router, prefix="/dal/publishing")
    app_.include_router(faker_router, prefix="/dal/faker")
    app_.include_router(gql_router, prefix="/dal/gql")

    return app_


app = create_app()
