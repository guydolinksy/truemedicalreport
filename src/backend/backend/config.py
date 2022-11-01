import json
import os

mongo_connection = json.loads(os.getenv('MONGO_CONNECTION', '"mongodb://localhost:27017"'))
redis_connection = json.loads(os.getenv('REDIS_CONNECTION', '"redis://localhost:6379"'))
dal_url = json.loads(os.getenv('DAL_CONNECTION', '""'))
ws_url = json.loads(os.getenv('SYNC_CONNECTION', '""'))
