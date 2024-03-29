from functools import cached_property
from typing import List, Dict, Tuple

from fastapi import Depends, HTTPException
from pymongo import MongoClient
from starlette.status import HTTP_510_NOT_EXTENDED
from werkzeug.local import LocalProxy

from .auth import AuthProvider
from .auth.local import LocalAuthProvider
from .exceptions import UnauthorizedException
from .user import User
from .. import config


class Authentication(object):
    def __init__(self, providers: List[AuthProvider]):
        self.providers: Dict[str, AuthProvider] = {provider.name: provider for provider in providers}
        assert len(providers) == len(self.providers), "Got multiple providers with the same name!"

    def _provider(self, name) -> AuthProvider:
        if provider := self.providers.get(name):
            if not provider.is_enabled():
                raise UnauthorizedException(f"Auth Provider '{name}' is disabled")

            return provider

        raise UnauthorizedException(f"Unsupported Auth Provider: '{name}'")

    def login(self, provider_name: str, *, username: str, password: str) -> Tuple[User, List[str]]:
        return self._provider(provider_name).login(username, password)


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
        self.general = Proxy(self.db.general, {})

        self.local_users = LocalAuthProvider(self.db.users)

        providers = [self.local_users]

        if config.LDAP_SUPPORTED:
            providers.append(self.ldap)

        self.auth = Authentication(providers)

    def for_user(self, username):
        return Proxy(self.db.settings, {'username': username})

    @cached_property
    def ldap(self) -> "LdapAuthProvider":  # type: ignore
        if config.LDAP_SUPPORTED:
            from .auth.ldap import LdapAuthProvider
            return LdapAuthProvider.with_settings_from_mongo(self.db.connections)

        raise HTTPException(
            status_code=HTTP_510_NOT_EXTENDED,
            detail=f"ldap login is not supported."
        )


def settings() -> Settings:
    return Settings(config.mongo_connection)


current_settings: LocalProxy[Settings] = LocalProxy(settings)


def _general_settings() -> Proxy:
    return current_settings.general


current_general_settings: LocalProxy[Proxy] = LocalProxy(_general_settings)


def general_settings(settings_=Depends(settings)) -> Proxy:
    return settings_.general
