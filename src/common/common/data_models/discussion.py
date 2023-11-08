import datetime
from typing import Optional, Dict

from pydantic import computed_field

from .base import Diffable


class Note(Diffable):
    follow_up_id: str
    at: str
    by: str
    content: str
    subject: Optional[str] = None

    @property
    def at_(self):
        return datetime.datetime.fromisoformat(self.at) if self.at else None

    @computed_field
    @property
    def external_id(self) -> str:
        return self.follow_up_id


class Discussion(Diffable):
    notes: Dict[str, Note] = {}

