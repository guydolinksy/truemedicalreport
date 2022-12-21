from typing import List

from pydantic import BaseModel


class User(BaseModel):
    username: str
    auth_provider_name: str
    is_admin: bool
    groups: List[str]
