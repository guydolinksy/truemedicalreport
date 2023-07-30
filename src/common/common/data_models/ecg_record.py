from pydantic import BaseModel
from typing import Optional


class ECGRecord(BaseModel):
    date: Optional[str]
    link: Optional[str]
    title: Optional[str]
