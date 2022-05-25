from enum import Enum

import pytz
from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from tmr_common.data_models.measures import Measure, MeasureTypes
from .base import Base


class MeasurementsIds(Enum):
    pulse = 12
    temperature = 11
    saturation = 13
    systolic = 101
    diastolic = 102


class ChameleonMeasurements(Base):
    __tablename__ = "measurements"

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
            type=MeasureTypes(MeasurementsIds(self.code).name),
            external_id=f'{self.patient_id}#{self.at.astimezone(pytz.UTC).isoformat()}#{self.code}',
        )
