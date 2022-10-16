from typing import Optional

from pydantic import BaseModel


class Admission(BaseModel):
    arrival: Optional[str]
    department: Optional[str]
    wing: Optional[str]
    bed: Optional[str]
