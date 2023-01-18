from typing import List

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration


def setup_sentry(dsn: str, extra_integrations: List[sentry_sdk.integrations.Integration] = None) -> None:
    """
    Initializes the Sentry SDK - further operations will be traced by Sentry.

    The Sentry integration injects itself to various places (FastAPI/Starlette, for example),
     in order to capture function calls and set HTTP headers, etc.

    Therefore, it must be initialized before anything else.

    :param dsn: See https://docs.sentry.io/product/sentry-basics/dsn-explainer/
    :param extra_integrations: Extra Sentry ingrations. By default, only the FastAPI integration is enabled.
    """
    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            *(extra_integrations or []),
            FastApiIntegration()
        ]
    )
