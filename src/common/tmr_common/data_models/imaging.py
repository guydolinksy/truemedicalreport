from enum import Enum
from typing import Optional

from pydantic import BaseModel

from tmr_common.data_models.notification import NotificationLevel


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
    type_: ImagingTypes
    status: ImagingStatus
    link: str
    level: NotificationLevel
    at: str

    class Config:
        orm_mode = True
