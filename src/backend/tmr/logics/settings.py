import shelve

from werkzeug.local import LocalProxy


def get_settings():
    return Settings()


class Settings(object):
    CONFIG_FILE_PATH = '/opt/config/settings.db'

    def __init__(self, path=CONFIG_FILE_PATH):
        self._path = path

    def __getattr__(self, item):
        with shelve.open(self._path) as src:
            return src.get(item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(Settings, self).__setattr__(key, value)
        with shelve.open(self._path) as src:
            src[key] = value


settings = LocalProxy(lambda: get_settings())
