import environs
import uvicorn
import sentry_sdk

env = environs.Env()

debug = env.bool("DEBUG")
port = env.int("PORT", 80)

sentry_dsn = env.str("SENTRY_CONNECTION_DSN", "")
sentry_sdk.init(sentry_dsn)

uvicorn.run("backend.app:app", host="0.0.0.0", port=port, debug=debug)
