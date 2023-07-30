from typing import Optional

from pydantic import BaseModel


class ECGRecord(BaseModel):
    date: Optional[str]
    link: Optional[str]
    title: Optional[str]
