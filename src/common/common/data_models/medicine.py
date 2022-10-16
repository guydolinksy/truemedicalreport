import datetime

from pydantic import BaseModel
from typing import Optional


class Medicine(BaseModel):
    label: Optional[str]
    dosage: Optional[str]
    given: Optional[str]
    since: Optional[str]

    @property
    def given_(self):
        return datetime.datetime.fromisoformat(self.given) if self.given else None

    @property
    def since_(self):
        return datetime.datetime.fromisoformat(self.since) if self.since else None

    @property
    def description(self):
        return f'{self.dosage} {self.label}'

    def get_instance_id(self):
        return f'{self.label}#{self.since.replace(":", "-")}'
