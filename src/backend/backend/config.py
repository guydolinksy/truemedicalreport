import json
import os

import logbook

logger = logbook.Logger("config")

mongo_connection = json.loads(os.getenv('MONGO_CONNECTION', '"mongodb://localhost:27017"'))
redis_connection = json.loads(os.getenv('REDIS_CONNECTION', '"redis://localhost:6379/1"'))
dal_url = json.loads(os.getenv('DAL_CONNECTION', '""'))

# Websocket tweaking.
# WS_CONSOLIDATION_WINDOW_SECONDS:
#   Makes the server wait up to this many seconds to make a single WS push.
#   Useful since we sometimes publish a large number of notifications in a short period of time.
#
# WS_BURST_THRESHOLD:
#   In case there's a very large burst (defined by this parameter), we won't wait for the consolidation time period
#   and notify the websockets right away just to prevent too large updates.
websocket_consolidation_window_seconds = json.loads(os.getenv("WS_CONSOLIDATION_WINDOW_SECONDS", '3'))
websocket_burst_threshold = json.loads(os.getenv("WS_BURST_THRESHOLD", '100'))


def __is_ldap_supported() -> bool:
    try:
        import ldap
        return True
    except ImportError:
        logger.warning("Note, LDAP login will be completely disabled because the ldap package is not installed.")
        return False


LDAP_SUPPORTED = __is_ldap_supported()
