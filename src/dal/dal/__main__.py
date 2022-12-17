import environs
import sentry_sdk
import uvicorn

env = environs.Env()

sentry_sdk.init("http://eae51195d27446ab834c64daf0e501e1@localhost:9000/3")

debug = env.bool('DEBUG')
port = env.int("DAL_PORT", 80)

uvicorn.run("dal.app:app", host="0.0.0.0", port=port, debug=debug)
