from .base import Base
from sqlalchemy import Column, VARCHAR, Integer, DateTime
from enum import Enum


class DescriptionCode(Enum):
    nurse_summarize = 901
    doctor_summarize = 900


class ChameleonMedicalFreeText(Base):
    __tablename__ = "medical_free_text"
    row_id = Column("Row_ID", Integer(), primary_key=True)
    medical_record = Column("Medical_Record", VARCHAR())
    documenting_date = Column("DocumentingDate", DateTime())
    documenting_time = Column("DocumentingTime", DateTime())
    unit_name = Column("unit_name", VARCHAR())
    unit = Column("Unit", VARCHAR())
    medical_text_code = Column("Description_code", VARCHAR())
    medical_text_title = Column("Description", VARCHAR())
    medical_text = Column("Description_Text", VARCHAR())
    documenting_user = Column("DocumentingUser", VARCHAR())
    source = Column("source", VARCHAR())
    inserted_date = Column("inserted_date", DateTime())
