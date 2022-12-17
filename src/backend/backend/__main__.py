import environs
import uvicorn
import sentry_sdk

env = environs.Env()

debug = env.bool("DEBUG")
port = env.int("PORT", 80)

sentry_sdk.init("http://4c6fa8c951c14d04b99773144cac8a72@localhost:9000/2")

uvicorn.run("backend.app:app", host="0.0.0.0", port=port, debug=debug)
