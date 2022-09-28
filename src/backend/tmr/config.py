import json
import os

mongo_connection = json.loads(os.getenv('MONGO_CONNECTION'))
redis_connection = json.loads(os.getenv('REDIS_CONNECTION'))
dal_url = json.loads(os.getenv('DAL_CONNECTION'))
ws_url = json.loads(os.getenv('SYNC_CONNECTION'))
