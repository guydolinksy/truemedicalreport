import json
import os

dal_url = json.loads(os.getenv('DAL_CONNECTION'))
arc_connection = json.loads(os.getenv('ARC_CONNECTION'))
