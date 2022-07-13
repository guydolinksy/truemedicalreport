from pydantic import BaseModel
from typing import Optional


class TreatmentDecision(BaseModel):
    decision: str
    destination: Optional[str]
