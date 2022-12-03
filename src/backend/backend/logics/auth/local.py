from typing import Optional

from pymongo.collection import Collection

from backend.logics.auth.base import AuthProvider
from backend.logics.exceptions import UnauthorizedException
from backend.logics.user import User


class LocalAuthProvider(AuthProvider):
    name = "local"

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def register(self, username: str, password: str) -> None:
        self.collection.update_one({'username': username}, {'$set': {'password': password}}, upsert=True)

    def login(self, username: str, password: str) -> Optional[User]:
        if doc := self.collection.find_one({'username': username}):
            if doc["password"] != password:
                # TODO: Proper salt+hash comparisons
                raise UnauthorizedException("Incorrect password")

            return User(
                username=username,
                auth_provider_name=self.name,
                is_admin=True,  # local users are always considered to be admins
                groups=[]
            )

        raise UnauthorizedException("Unknown user")
