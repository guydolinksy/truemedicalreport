from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    auth_provider_name: str
    plugin_token: Optional[str] = None

    is_admin: bool = False
    view_only: bool = False
    anonymous: bool = False
