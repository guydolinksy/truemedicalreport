from typing import List, Optional

import interruptingcow
from fastapi import Depends
from fastapi_login.exceptions import InvalidCredentialsException
from pymongo import MongoClient
from pymongo.collection import Collection
from werkzeug.local import LocalProxy

from .ldap_auth import LdapAuth
from .user import User
from .. import config


class Connection:
    def register(self, username: str, password: str) -> None:
        raise NotImplementedError

    def login(self, username: str, password: str) -> Optional[User]:
        raise NotImplementedError


class LocalConnection(Connection):
    mode = 'local'

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def register(self, username: str, password: str) -> None:
        self.collection.update_one({'username': username}, {'$set': {'password': password}}, upsert=True)

    def login(self, username: str, password: str) -> Optional[User]:
        if self.collection.find_one({'username': username, 'password': password}):
            return User(
                username=username,
                source=self.mode,
                is_admin=True,  # local users are always considered to be admins
                groups=[]
            )

    def has_user(self, username: str) -> bool:
        return bool(self.collection.find_one({'username': username}))


class LDAPConnection(Connection):
    mode = 'ldap'

    def __init__(self, collection: Collection):
        self.collection = collection

    @property
    def settings(self) -> LdapAuth:
        if res := self.collection.find_one({'type': self.mode}):
            del res["_id"]
            del res["type"]
            return LdapAuth(**res)

        return LdapAuth(enabled=False)

    def update_settings(self, new_settings: dict) -> None:
        try:
            LdapAuth(**new_settings)
        except Exception:
            raise Exception("The new settings are invalid")

        self.collection.replace_one({'type': self.mode}, {
            "type": self.mode,
            **new_settings
        }, upsert=True)

    def register(self, username: str, password: str) -> None:
        raise Exception("Registering users with LDAP is not supported")

    def login(self, username: str, password: str) -> Optional[User]:
        with interruptingcow.timeout(seconds=5, exception=TimeoutError):
            return self.settings.auth_with_groups(login_source=self.mode, username=username, password=password)


class Authentication(object):
    def __init__(self, connections: List[Connection]):
        self.connections = connections

    def login(self, username: str, password: str) -> User:
        for c in self.connections:
            if user := c.login(username, password):
                return user
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

        self.local_users = LocalConnection(self.db.users)
        self.ldap = LDAPConnection(self.db.connections)
        self.auth = Authentication([self.local_users, self.ldap])

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
