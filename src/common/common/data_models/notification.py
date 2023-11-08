from enum import Enum
from typing import Optional

from .base import Diffable


class NotificationLevel(int, Enum):
    normal = 0
    abnormal = 1
    panic = 2
    unknown = -1


class NotificationType(str, Enum):
    lab = 'labs'
    imaging = 'imaging'
    referral = 'referral'
    general = 'general'


class Notification(Diffable):
    static_id: str
    message: str
    at: str
    type_: NotificationType
    level: NotificationLevel
    link: Optional[str] = None

