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
    referral = 'refferals'
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


class ImagingNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {kwargs['type'].value: kwargs['static_id']}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.imaging
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(ImagingNotification, self).__init__(**kwargs)


class LabsNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {kwargs['type'].value: kwargs['static_id']}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.lab
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(LabsNotification, self).__init__(**kwargs)


class ReferralsNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {kwargs['type'].value: kwargs['static_id']}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.referral
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(ReferralsNotification, self).__init__(**kwargs)
