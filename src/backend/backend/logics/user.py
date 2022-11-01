from typing import List

from pydantic import BaseModel


class User(BaseModel):
    username: str
    source: str
    is_admin: bool
    groups: List[str]
