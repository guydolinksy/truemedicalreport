import json
import os

dal_url = json.loads(os.getenv('DAL_CONNECTION'))
db_connection = json.loads(os.getenv('DB_CONNECTION'))
