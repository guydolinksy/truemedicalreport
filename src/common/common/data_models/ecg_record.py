from typing import Optional

from .base import Diffable


class ECGRecord(Diffable):
    date: Optional[str]
    link: Optional[str]
    title: Optional[str]

