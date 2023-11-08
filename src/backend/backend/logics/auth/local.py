from typing import Tuple, List

from pymongo.collection import Collection

from backend.logics.auth.base import AuthProvider
from backend.logics.exceptions import UnauthorizedException
from backend.logics.user import User


class LocalAuthProvider(AuthProvider):
    name = "local"

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def register(self, username: str, password: str, **settings) -> None:
        self.collection.update_one(
            {'username': username},
            {'$set': dict(password=password, **{f'settings.{k}': v for k, v in settings.items()})},
            upsert=True
        )

    def login(self, username: str, password: str) -> Tuple[User, List[str]]:
        if doc := self.collection.find_one({'username': username}):
            if doc["password"] != password:
                # TODO: Proper salt+hash comparisons
                raise UnauthorizedException("Incorrect password")

            return User(
                username=username,
                auth_provider_name=self.name,
                is_admin=doc.get('settings', {}).get('is_admin', False),
                view_only=doc.get('settings', {}).get('view_only', False),
                anonymous=doc.get('settings', {}).get('anonymous', False),
            ), []

        raise UnauthorizedException("Unknown user")
