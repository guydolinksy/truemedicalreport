from enum import Enum

from pydantic import BaseModel

from common.data_models.notification import NotificationLevel, Notification, NotificationType


class ImagingTypes(Enum):
    ct = 'ct'
    ultrasound = 'us'
    xray = 'xray'


class ImagingStatus(Enum):
    ordered = 'ordered'
    performed = 'performed'
    analyzed = 'analyzed'
    verified = 'verified'


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
    external_id: str
    patient_id: str
    title: str
    status: ImagingStatus
    status_text: str
    link: str
    level: NotificationLevel
    at: str

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
            }[kwargs['status']]

        super(Image, self).__init__(**kwargs)

    def to_notification(self) -> ImagingNotification:
        return ImagingNotification(
            static_id=self.external_id,
            patient_id=self.patient_id,
            at=self.at,
            message=f'{self.title} - {self.status_text}',
            link=self.link,
            level=self.level,
        )
