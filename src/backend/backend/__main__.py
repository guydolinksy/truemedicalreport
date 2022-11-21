import environs
import uvicorn

env = environs.Env()

debug = env.bool("DEBUG")
port = env.int("PORT", 80)

uvicorn.run("backend.app:app", host="0.0.0.0", port=port, debug=debug)
