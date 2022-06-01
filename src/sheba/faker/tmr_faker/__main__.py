import os

import uvicorn

debug = bool(os.environ.get('DEBUG'))

uvicorn.run("tmr_faker.app:app", host="0.0.0.0", port=80, debug=debug)
