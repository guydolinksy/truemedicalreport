import json
import os

import logbook

logger = logbook.Logger("config")

mongo_connection = json.loads(os.getenv('MONGO_CONNECTION', '"mongodb://localhost:27017"'))
redis_connection = json.loads(os.getenv('REDIS_CONNECTION', '"redis://localhost:6379/1"'))
dal_url = json.loads(os.getenv('DAL_CONNECTION', '""'))


def __is_ldap_supported() -> bool:
    try:
        import ldap
        return True
    except ImportError:
        logger.warning("Note, LDAP login will be completely disabled because the ldap package is not installed.")
        return False


LDAP_SUPPORTED = __is_ldap_supported()
