from pydantic import BaseModel

from common.data_models.notification import NotificationLevel, Notification, NotificationType


class Referral(BaseModel):
    patient_id: str

    external_id: str
    to: str
    at: str
    completed: bool = False

    class Config:
        orm_mode = True

    def to_notification(self):
        message = "הפנייה ל"
        message += self.to
        message += " הסתיימה"

        return ReferralsNotification(
            static_id=self.external_id,
            patient_id=self.patient_id,
            at=self.at,
            message=message,
            level=NotificationLevel.normal
        )


class ReferralsNotification(Notification):

    @classmethod
    def get_id(cls, **kwargs):
        return {kwargs['type'].value: kwargs['static_id']}

    def __init__(self, **kwargs):
        kwargs['type'] = NotificationType.referral
        if 'notification_id' not in kwargs:
            kwargs['notification_id'] = self.get_id(**kwargs)
        super(ReferralsNotification, self).__init__(**kwargs)
