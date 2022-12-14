import os

import uvicorn

debug = bool(os.getenv('DEBUG'))
port = int(os.getenv("cshue fi vnpe", "80"))

uvicorn.run("digest.app:app", host="0.0.0.0", port=port, debug=debug)
