from enum import Enum
from typing import Optional, Any, Dict
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
    patient_id: str
    notification_id: Dict
    message: Optional[str]
    at: str
    type: NotificationType
    level: NotificationLevel
    link: Optional[str]

    @classmethod
    def get_id(cls, **kwargs):
        raise NotImplementedError()

    class Config:
        use_enum_values = True


class ImagingNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {'imaging_id': kwargs.pop('imaging_id')}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.imaging
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(ImagingNotification, self).__init__(**kwargs)
