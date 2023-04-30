import json
import os

dal_url = json.loads(os.getenv('DAL_CONNECTION'))
chameleon_connection = json.loads(os.getenv('CHAMELEON_CONNECTION'))
oracle_params = json.loads(os.getenv('ORACLE_CONNECTION'))
sentry_dsn = os.getenv('SENTRY_DSN', None)
