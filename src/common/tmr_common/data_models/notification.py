from enum import Enum
from typing import Optional
from pydantic import BaseModel


class NotificationLevel(Enum):
    panic = 1
    abnormal = 2
    normal = 3


class NotificationType(Enum):
    lab = 'labs'
    imaging = 'imaging'
    consult = 'consults'
    general = 'general'


class Notification(BaseModel):
    message: Optional[str]
    at: str
    type: NotificationType
    level: NotificationLevel

    class Config:
        orm_mode = True


class ImagingNotification(Notification):
    class Config:
        orm_mode = True

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.imaging
        super(ImagingNotification, self).__init__(**kwargs)


