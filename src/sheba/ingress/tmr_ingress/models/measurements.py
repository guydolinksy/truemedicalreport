from enum import Enum

from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from tmr_common.data_models.measures import Measurement
from .base import Base


class MeasurementsIds(Enum):
    systolic = 101
    diastolic = 102
    temperature = 11
    pulse = 12
    saturation = 13


class Measurements(Base):
    __tablename__ = "measurements"

    pk = Column("pk_measurement_id", Integer(), primary_key=True)
    chameleon_id = Column("id_num", VARCHAR(200))
    at = Column("Parameter_Date", DateTime())
    code = Column("Parameter_Id", Integer())
    name = Column("Parameter_Name", VARCHAR(100))
    value = Column("Result", Float())
    min_limit = Column("Min_Value", Float())
    max_limit = Column("Max_Value", Float())
    warnings = Column("Warnings", VARCHAR(100))

    def to_dal(self):
        return Measurement(
            at=self.at.isoformat(),
            value=self.value,
            minimum=self.min_limit,
            maximum=self.max_limit,
        )
