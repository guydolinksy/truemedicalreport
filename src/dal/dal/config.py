import json
import os

mongo_connection = json.loads(os.getenv('MONGO_CONNECTION'))
redis_connection = json.loads(os.getenv('REDIS_CONNECTION'))
arc_connection = json.loads(os.getenv('ARC_CONNECTION'))
sentry_dsn = os.getenv('SENTRY_DSN', None)
