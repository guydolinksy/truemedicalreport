from typing import Optional

from pydantic import computed_field

from .base import Diffable
from .notification import NotificationLevel, Notification, NotificationType


class Referral(Diffable):
    to: str
    at: str
    completed_at: Optional[str] = None


    @computed_field
    @property
    def external_id(self) -> str:
        return f'referral#{self.at.replace(":", "-").replace(".", "-")}'

    def to_notifications(self):
        n = ReferralsNotification(
            static_id=self.external_id,
            at=self.at,
            message=f"הפנייה ל{self.to} הסתיימה",
            level=NotificationLevel.normal
        )
        return {n.static_id: n}


class ReferralsNotification(Notification):
    type: NotificationType = NotificationType.referral

