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
    chameleon_id: int
    patient_id: str
    type_: ImagingTypes
    status: ImagingStatus
    link: str
    level: NotificationLevel
    at: str

    class Config:
        orm_mode = True
        use_enum_values = True
        # TODO add the flag to all classes that using enum

    def to_notification(self):
        return ImagingNotification(
            imaging_id=self.chameleon_id,
            patient_id=self.patient_id,
            at=self.at,
            message=f'{self.type_} - {self.status}\n{self.link}',
            level=self.level,
        )
