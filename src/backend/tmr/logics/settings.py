from typing import List, Optional

import interruptingcow
import ldap
from fastapi import Depends
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from werkzeug.local import LocalProxy

from .. import config


class Connection(object):
    mode = NotImplemented

    def __contains__(self, item):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def connect(self, username, password):
        return (username, password) in self


class LocalConnection(Connection):
    mode = 'local'

    def __init__(self, collection):
        self.collection = collection

    def __contains__(self, item):
        username, password = item
        return self.collection.find_one({'username': username, 'password': password})

    def __getitem__(self, key):
        return self.collection.find_one({'username': key}, {'password': 0})

    def __setitem__(self, key, value):
        self.collection.update_one({'username': key}, {'$set': {'password': value}}, upsert=True)


class LDAPConnection(Connection):
    mode = 'ldap'

    def __init__(self, collection: Collection):
        self.collection = collection

    @property
    def settings(self):
        res = self.collection.find_one({'type': 'ldap'})
        return LDAP(**(res or {}))

    @settings.setter
    def settings(self, value):
        self.collection.update_one({'type': 'ldap'}, {'$set': value})

    def __contains__(self, item):
        if not self.settings.enabled:
            return False

        username, password = item

        with interruptingcow.timeout(seconds=5, exception=TimeoutError):
            connection = ldap.initialize(self.settings.connection)
            return connection.bind_s(self.settings.user_dn.format(username), password)

    def __setitem__(self, key, value):
        raise NotImplementedError


class LDAP(BaseModel):
    enabled: bool = False
    connection: Optional[str]
    user_dn: Optional[str]
    bind_dn: Optional[str]
    bind_password: Optional[str]
    admin_ou: Optional[str]
    users_ou: Optional[str]


class Authentication(object):
    def __init__(self, connections: List[Connection]):
        self.connections = connections

    def connect(self, username, password):
        for c in self.connections:
            if c.connect(username, password):
                return c.mode
        else:
            raise InvalidCredentialsException


class Proxy(object):
    def __init__(self, collection, query):
        self._collection = collection
        self._query = query

    def __getattr__(self, item):
        res = self._collection.find_one(self._query, {item: 1})
        if not res or item not in res:
            raise AttributeError()
        return res[item]

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(Proxy, self).__setattr__(key, value)
        return self._collection.update_one(self._query, {'$set': {key: value}}, upsert=True)


class Settings(object):
    def __init__(self, connection):
        self.db = MongoClient(connection).app

        self.users = LocalConnection(self.db.users)
        self.ldap = LDAPConnection(self.db.connections)
        self.auth = Authentication([self.users, self.ldap])

        self.general = Proxy(self.db.general, {})

    def for_user(self, username):
        return Proxy(self.db.settings, {'username': username})


def settings() -> Settings:
    return Settings(config.mongo_connection)


current_settings: LocalProxy[Settings] = LocalProxy(settings)


def _general_settings() -> Proxy:
    return current_settings.general


current_general_settings: LocalProxy[Proxy] = LocalProxy(_general_settings)


def general_settings(settings_=Depends(settings)) -> Proxy:
    return settings_.general
