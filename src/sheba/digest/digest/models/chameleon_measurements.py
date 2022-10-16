from enum import Enum

import pytz
from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from common.data_models.measures import Measure, MeasureType
from .base import Base


class MeasurementsIds(Enum):
    pain = 14
    pulse = 12
    temperature = 11
    saturation = 13
    systolic = 101
    diastolic = 102


class ChameleonMeasurements(Base):
    __tablename__ = "measurements"
    __table_args__ = {"schema": "dw"}

    patient_id = Column("id", VARCHAR(200), primary_key=True)
    at = Column("entry_time", DateTime(), primary_key=True)
    code = Column("ParameterCode", Integer(), primary_key=True)
    name = Column("Parameter_Name", VARCHAR(100))
    value = Column("Result", Float())
    min_limit = Column("Min_Value", Float())
    max_limit = Column("Max_Value", Float())

    def to_dal(self):
        return Measure(
            value=self.value,
            minimum=self.min_limit,
            maximum=self.max_limit,
            at=self.at.astimezone(pytz.UTC).isoformat(),
            type=MeasureType(MeasurementsIds(self.code).name),
            external_id=f'{self.patient_id}#{self.at.astimezone(pytz.UTC).isoformat()}#{self.code}',
        )
