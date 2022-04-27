from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Imaging(Base):
    __tablename__ = "imaging"

    patient_id = Column("patient_id", VARCHAR(250), primary_key=True)
    imaging_id = Column("imaging_id", Integer())
    imaging_name = Column("imaging_name", VARCHAR(60))
    result = Column("result_name", VARCHAR(100))
    date = Column("result_date", DateTime())
