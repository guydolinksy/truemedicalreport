from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ESIScore(BaseModel):
    value: Optional[int]
    at: Optional[str]
