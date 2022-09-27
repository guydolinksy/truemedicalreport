from pydantic import BaseModel
from typing import Optional


class Medicine(BaseModel):
    label: Optional[str]
    dosage: Optional[str]
    is_given: Optional[bool]
