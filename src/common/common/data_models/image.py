from enum import Enum

from pydantic import BaseModel
from typing import Optional
from common.data_models.notification import NotificationLevel, Notification, NotificationType


class ImagingTypes(Enum):
    ct = 'ct'
    ultrasound = 'us'
    xray = 'xray'
    mri = 'mri'
    unknown = 'unknown'


class ImagingStatus(Enum):
    ordered = 1
    performed = 2
    analyzed = 3
    verified = 4
    cancelled = 5
    unknown = 6


class ImagingNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {kwargs['type'].value: kwargs['static_id']}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.imaging
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(ImagingNotification, self).__init__(**kwargs)


class Image(BaseModel):
    order_number: Optional[str]
    external_id: str
    patient_id: str
    title: str
    status: ImagingStatus
    code: Optional[int]
    imaging_type: Optional[ImagingTypes]
    status_text: str
    link: str
    level: NotificationLevel
    ordered_at: str
    updated_at: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
        # TODO add the flag to all classes that using enum

    def __init__(self, **kwargs):
        if 'status_text' not in kwargs:
            kwargs['status_text'] = {
                ImagingStatus.ordered: 'הוזמן',
                ImagingStatus.performed: 'בוצע',
                ImagingStatus.analyzed: 'פוענח',
                ImagingStatus.verified: 'אושרר',
                ImagingStatus.cancelled: 'בוטל',
                ImagingStatus.unknown: 'לא ידוע',
            }[kwargs['status']]

        super(Image, self).__init__(**kwargs)

    def to_notification(self) -> ImagingNotification:
        return ImagingNotification(
            static_id=self.external_id,
            patient_id=self.patient_id,
            at=self.accomplished_at if self.accomplished_at else self.ordered_at,
            message=f'{self.title} - {self.status_text}',
            link=self.link,
            level=self.level,
        )
