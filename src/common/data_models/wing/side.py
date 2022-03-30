from pydantic import BaseModel
from typing import List, Optional


class Side(BaseModel):
    name: str
    beds: Optional[List[str]]
