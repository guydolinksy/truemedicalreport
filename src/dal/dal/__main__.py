import environs
import uvicorn

env = environs.Env()

debug = env.bool('DEBUG')
port = env.int("DAL_PORT", 80)

uvicorn.run("dal.app:app", host="0.0.0.0", port=port, debug=debug)
