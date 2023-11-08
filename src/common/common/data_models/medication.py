import datetime
from typing import Optional

from pydantic import computed_field

from .base import Diffable


class Medication(Diffable):
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

    @computed_field
    @property
    def external_id(self) -> str:
        return f'{self.label}#{self.since.replace(":", "-").replace(".", "-")}'
