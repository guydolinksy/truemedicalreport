import datetime
from enum import Enum

import pytz
from sqlalchemy import Column, VARCHAR, DateTime, Date, BigInteger

from tmr_common.data_models.patient import Intake
from .base import Base


class FreeTextCodes(Enum):
    DOCTOR_VISIT = 1
    DOCTOR_SUMMARY = 889
    NURSE_SUMMARY = 901


class Units(Enum):
    ER = 1184000



class ChameleonMedicalText(Base):
    __tablename__ = "medical_free_text"
    __table_args__ = {"schema": "dw"}

    row_id = Column("Row_ID", BigInteger(), primary_key=True)
    patient_id = Column("Id", BigInteger())
    medical_record = Column("Medical_Record", BigInteger())
    documenting_date = Column("DocumentingDate", Date())
    documenting_time = Column("DocumentingTime", DateTime())
    unit_name = Column("unit_name", VARCHAR(80))
    unit = Column("Unit", BigInteger())
    medical_text_code = Column("Description_code", BigInteger())
    medical_text_title = Column("Description", VARCHAR(500))
    medical_text = Column("Description_Text", VARCHAR())
    documenting_user = Column("DocumentingUser", BigInteger())
    source = Column("source", VARCHAR(), default="chameleon")
    # date of inserting the row to ARC db
    insert_date = Column("insert_date", DateTime(), default=datetime.datetime.utcnow())

    def update_intake(self, intake: Intake):
        if self.medical_text_code == FreeTextCodes.NURSE_SUMMARY.value:
            intake.nurse_description = self.medical_text
            intake.nurse_seen_time = self.documenting_time.astimezone(pytz.UTC).isoformat()
        elif self.medical_text_code == FreeTextCodes.DOCTOR_VISIT.value:
            intake.doctor_seen_time = self.documenting_time.astimezone(pytz.UTC).isoformat()
