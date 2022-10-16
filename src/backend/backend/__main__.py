import os

import uvicorn

debug = bool(os.getenv('DEBUG'))

uvicorn.run("backend.app:app", host="0.0.0.0", port=80, debug=debug)
