from enum import Enum
from typing import Optional, Dict

import logbook
from pydantic import computed_field

from common.data_models.notification import NotificationLevel, Notification, NotificationType
from .base import Diffable

logger = logbook.Logger(__name__)


class ImagingTypes(str, Enum):
    ct = 'ct'
    ultrasound = 'us'
    xray = 'xray'
    mri = 'mri'
    unknown = 'unknown'


class ImagingStatus(int, Enum):
    ordered = 1
    performed = 2
    analyzed = 3
    verified = 4
    cancelled = 5
    unknown = 6


class ImagingNotification(Notification):
    type_: NotificationType = NotificationType.imaging


class Image(Diffable):
    order_number: str
    accession_number: str
    title: str
    status: ImagingStatus
    imaging_type: Optional[ImagingTypes] = None
    link: str
    interpretation: Optional[str] = None
    level: NotificationLevel
    ordered_at: str
    updated_at: str

    @computed_field
    @property
    def external_id(self) -> str:
        return self.accession_number

    @computed_field
    @property
    def status_text(self) -> str:
        return {
            ImagingStatus.ordered: 'הוזמן',
            ImagingStatus.performed: 'בוצע',
            ImagingStatus.analyzed: 'פוענח',
            ImagingStatus.verified: 'אושרר',
            ImagingStatus.cancelled: 'בוטל',
            ImagingStatus.unknown: 'לא ידוע',
        }[self.status]

    def to_notifications(self) -> Dict[str, ImagingNotification]:
        i = ImagingNotification(
            static_id=self.external_id,
            at=self.updated_at if self.updated_at else self.ordered_at,
            message=f'{self.title} - {self.status_text}',
            link=self.link,
            level=self.level,
        )
        return {i.static_id: i}

    def _is_completed(self) -> bool:
        # logger.debug(f"{self}")
        if self.imaging_type == ImagingTypes.xray:
            result = self.status in [ImagingStatus.verified, ImagingStatus.analyzed,
                                     ImagingStatus.cancelled, ImagingStatus.performed]
            # logger.debug(f"xray - {self}")

            return result
        return self.status in [ImagingStatus.verified, ImagingStatus.analyzed,
                               ImagingStatus.cancelled]
