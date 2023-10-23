from typing import Optional

from .base import Diffable


class MCIStringValue(Diffable):
    value: Optional[str] = None
    at: Optional[str] = None


class MCIBooleanValue(Diffable):
    value: Optional[bool] = None
    at: Optional[str] = None
