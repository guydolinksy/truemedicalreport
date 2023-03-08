from typing import Optional, Dict

from pydantic import BaseModel


class Protocol(BaseModel):
    title: Optional[str]
    attributes: Optional[Dict[str, str]]
