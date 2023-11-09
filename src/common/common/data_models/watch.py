import datetime
from typing import Optional

from common.data_models.base import Diffable, ParsableMixin


class WatchKey(Diffable, ParsableMixin):
    update_at: Optional[str] = None
    triggered: bool = False
    watched: bool = False
    message: Optional[str] = None

    @property
    def update_at_(self):
        return datetime.datetime.fromisoformat(self.update_at) if self.update_at else None

    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        return cls(**value)
