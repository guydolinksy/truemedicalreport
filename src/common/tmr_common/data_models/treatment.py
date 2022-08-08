from typing import Optional

from pydantic import BaseModel


class Treatment(BaseModel):
    destination: Optional[str]
