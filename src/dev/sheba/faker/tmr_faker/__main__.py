import os

import uvicorn

debug = bool(os.getenv('DEBUG'))
port = int(os.getenv("FAKER_PORT", "80"))

uvicorn.run("tmr_faker.app:app", host="0.0.0.0", port=port, debug=debug)
