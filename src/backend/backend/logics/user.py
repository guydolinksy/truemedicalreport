from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    auth_provider_name: str
    is_admin: bool
    groups: List[str]
    plugin_token: Optional[str]
