from pydantic import BaseModel

from tmr_common.data_models.notification import ReferralsNotification, NotificationLevel


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
