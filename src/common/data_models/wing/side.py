from pydantic import BaseModel
from typing import List


class Side(BaseModel):
    name: str
    beds: List[str]
