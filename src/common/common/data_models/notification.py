from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel


class NotificationLevel(Enum):
    normal = 0
    abnormal = 1
    panic = 2
    unknown = -1


class NotificationType(Enum):
    lab = 'labs'
    imaging = 'imaging'
    referral = 'referral'
    general = 'general'


class Notification(BaseModel):
    patient_id: str
    notification_id: Dict
    static_id: str
    message: str
    at: str
    type: NotificationType
    level: NotificationLevel
    link: Optional[str]

    @classmethod
    def get_id(cls, **kwargs):
        raise NotImplementedError()

    class Config:
        use_enum_values = True
