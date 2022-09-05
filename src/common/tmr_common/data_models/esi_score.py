from pydantic import BaseModel
from typing import Optional


class ESIScore(BaseModel):
    value: Optional[int]
    at: Optional[str]
