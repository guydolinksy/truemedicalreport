from typing import Optional, List

from pydantic import BaseModel


class Treatment(BaseModel):
    destination: Optional[str]
    doctors: List[str] = list()
