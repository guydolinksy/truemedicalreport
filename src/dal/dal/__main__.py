import environs
import sentry_sdk
import uvicorn

env = environs.Env()

debug = env.bool('DEBUG')
port = env.int("DAL_PORT", 80)

sentry_dsn = env.str("SENTRY_CONNECTION_DSN")
sentry_sdk.init(sentry_dsn)

uvicorn.run("dal.app:app", host="0.0.0.0", port=port, debug=debug)
