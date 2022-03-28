import os

import uvicorn

debug = bool(os.environ.get('DEBUG'))

uvicorn.run("tmr.app:app", host="0.0.0.0", port=8050, debug=debug)
