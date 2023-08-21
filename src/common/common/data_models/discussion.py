import datetime
from typing import Optional, Dict

from pydantic import BaseModel


class Note(BaseModel):
    content: Optional[str]
    subject: Optional[str]
    at: Optional[str]
    by: Optional[str]

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at) if self.at else None

class Discussion(BaseModel):
    notes: Dict[str, Note] = {}
