from pydantic import BaseModel

from tmr_common.data_models.notification import ReferralsNotification, NotificationLevel


class Referral(BaseModel):
    external_id: str
    patient_id: int
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
            static_id=self.get_instance_id(),
            patient_id=self.patient_id,
            at=self.at,
            message=message,
            level=NotificationLevel.normal
        )
