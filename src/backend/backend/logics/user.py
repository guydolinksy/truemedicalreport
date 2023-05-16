from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    auth_provider_name: str
    plugin_token: Optional[str]

    is_admin: bool = False
    view_only: bool = False
    anonymous: bool = False
