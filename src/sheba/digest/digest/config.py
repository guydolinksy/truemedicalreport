import json
import os

dal_url = json.loads(os.getenv('DAL_CONNECTION'))
chameleon_connection = json.loads(os.getenv('CHAMELEON_CONNECTION'))
