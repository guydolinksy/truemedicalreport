import os
import sentry_sdk
import uvicorn

sentry_sdk.init("http://a9534e831da44d579276aca9718149ec@localhost:9000/5")

debug = bool(os.getenv('DEBUG'))
port = int(os.getenv("FAKER_PORT", "80"))

uvicorn.run("tmr_faker.app:app", host="0.0.0.0", port=port, debug=debug)
