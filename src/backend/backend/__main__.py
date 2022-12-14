import environs
import uvicorn

env = environs.Env()

debug = env.bool("DEBUG")
port = env.int("TMR_BACKEND_PORT", 80)

uvicorn.run("backend.app:app", host="0.0.0.0", port=port, debug=debug)
