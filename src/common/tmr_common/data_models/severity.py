from typing import Optional

from pydantic import BaseModel


class Severity(BaseModel):
    value: Optional[int]
    at: Optional[str]
