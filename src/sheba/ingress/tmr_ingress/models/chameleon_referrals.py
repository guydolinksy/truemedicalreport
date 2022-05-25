import pytz
from sqlalchemy import VARCHAR, Integer, Column, DateTime, BINARY

from tmr_common.data_models.referrals import Referral
from .base import Base


class ChameleonReferrals(Base):
    __tablename__ = "referrals"

    referral_code = Column("ReferralCode", Integer(), primary_key=True)
    patient_id = Column("id", Integer())
    to = Column("DoctorName", VARCHAR(50))
    order_date = Column("OrderDate", DateTime())
    completion_date = Column("CompletedDate", VARCHAR(100))

    def to_dal(self):
        return Referral(
            external_id=f"{self.patient_id}#{self.referral_code}",
            patient_id=self.patient_id,
            to=self.to,
            at=self.order_date.astimezone(pytz.UTC).isoformat(),
            completed=bool(self.completion_date),
        )
