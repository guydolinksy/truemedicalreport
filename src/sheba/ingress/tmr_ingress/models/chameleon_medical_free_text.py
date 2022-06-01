import datetime

from .base import Base
from sqlalchemy import Column, VARCHAR, Integer, DateTime, Date, BigInteger
from enum import Enum


class DescriptionCode(Enum):
    nurse_summarize = 901
    doctor_summarize = 900


class ChameleonMedicalFreeText(Base):
    __tablename__ = "medical_free_text"
    row_id = Column("Row_ID", BigInteger())
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
    inserted_date = Column("inserted_date", DateTime(), default=datetime.datetime.utcnow())
