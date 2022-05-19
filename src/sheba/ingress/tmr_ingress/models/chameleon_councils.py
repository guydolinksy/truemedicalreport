from sqlalchemy import VARCHAR, Integer, Column, DateTime, BINARY

from tmr_common.data_models.councils import Councils
from .base import Base


class ChameleonCouncils(Base):
    __tablename__ = "councils"

    council_code = Column("CouncilCode", Integer(), primary_key=True)
    patient_id = Column("id", Integer())
    council_name = Column("CouncilName", VARCHAR(50))
    doctor_id = Column("DoctorId", Integer())
    doctor_name = Column("DoctorName", VARCHAR(50))
    order_date = Column("OrderDate", DateTime())
    council_date = Column("CouncilDate", VARCHAR(100))
    arrived = Column("Arrived", BINARY(100))

    def to_dal(self):
        return Councils(
            external_id=f"{self.patient_id}#{self.council_code}",
            patient_id=self.patient_id,
            council_name=self.council_name,
            doctor_id=self.doctor_id,
            doctor_name=self.doctor_name,
            at=self.order_date.isoformat(),
            council_date=self.council_date.isoformat(),
            arrived=self.arrived,
        )
