import environs
import uvicorn

env = environs.Env()

debug = env.bool("TMR_BACKEND_DEBUG")
port = env.int("TMR_BACKEND_PORT", 8080)

uvicorn.run("backend.app:app", host="0.0.0.0", port=port, debug=debug)
