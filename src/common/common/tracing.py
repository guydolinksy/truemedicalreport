import os
from typing import List

import logbook
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration


logger = logbook.Logger("tracing")


def setup_sentry(dsn: str, extra_integrations: List[sentry_sdk.integrations.Integration] = None) -> None:
    """
    Initializes the Sentry SDK - further operations will be traced by Sentry.

    The Sentry integration injects itself to various places (FastAPI/Starlette, for example),
     in order to capture function calls and set HTTP headers, etc.

    Therefore, it must be initialized before anything else.

    :param dsn: See https://docs.sentry.io/product/sentry-basics/dsn-explainer/
    :param extra_integrations: Extra Sentry ingrations. By default, only the FastAPI integration is enabled.
    """
    if sentry_ca_path := os.getenv("SENTRY_CA_CERT_PATH"):
        logger.info(f"Note, using CA from {sentry_ca_path}")
        assert os.path.exists(sentry_ca_path), "The provided CA path doesn't exist"

    sentry_sdk.init(
        dsn=dsn,
        ca_certs=sentry_ca_path,
        integrations=[
            *(extra_integrations or []),
            FastApiIntegration()
        ]
    )
