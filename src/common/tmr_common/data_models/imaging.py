from enum import Enum
from typing import Optional

from pydantic import BaseModel

from tmr_common.data_models.notification import NotificationLevel, ImagingNotification


class ImagingTypes(Enum):
    ct = 'ct'
    ultrasound = 'us'
    xray = 'xray'


class ImagingStatus(Enum):
    ordered = 'ordered'
    performed = 'performed'
    analyzed = 'analyzed'
    verified = 'verified'


class Imaging(BaseModel):
    external_id: int
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

        super(Imaging, self).__init__(**kwargs)

    def to_notification(self):
        return ImagingNotification(
            static_id=self.external_id,
            patient_id=self.patient_id,
            at=self.at,
            message=f'{self.title} - {self.status_text}',
            link=self.link,
            level=self.level,
        )
