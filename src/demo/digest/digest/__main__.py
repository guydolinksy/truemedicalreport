import os
import sentry_sdk
import uvicorn

sentry_sdk.init("http://9a01350b1137400f8abe55a6bf140c08@localhost:9000/4")

debug = bool(os.getenv('DEBUG'))
port = int(os.getenv("DIGEST_PORT", "80"))

uvicorn.run("digest.app:app", host="0.0.0.0", port=port, debug=debug)
