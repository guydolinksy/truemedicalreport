from typing import Optional

from pydantic import BaseModel


class WatchKey(BaseModel):
    update_at: str
    triggered: bool = False
    watched: bool = False
    message: Optional[str]


