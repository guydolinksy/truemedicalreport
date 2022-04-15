from typing import Optional

from pydantic import BaseModel

from .patient import Patient


class Bed(BaseModel):
    patient: Optional[str]

    class Config:
        orm_mode = True
