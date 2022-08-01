from typing import Optional

from pydantic import BaseModel


class Bed(BaseModel):
    patient: Optional[str]

    class Config:
        orm_mode = True
