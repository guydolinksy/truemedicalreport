from enum import Enum

from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base
from tmr_common.data_models.imaging import Imaging

Base = declarative_base()


class ImagingIds(Enum):
    ct = 1
    ultrasound = 2
    radiography = 3


class ImagingResultsIds(Enum):
    ordered = 1
    executed = 2
    deciphered = 3
    approved = 4


class ChameleonImaging(Base):
    __tablename__ = "imaging"

    patient_id = Column("patient_id", VARCHAR(250), primary_key=True)
    imaging_id = Column("imaging_id", Integer())
    imaging = Column("imaging_name", VARCHAR(60))
    result_id = Column("result_id", VARCHAR(100))
    result = Column("result_name", VARCHAR(100))
    link = Column("link", VARCHAR(100))
    at = Column("result_date", DateTime())

    def to_dal(self):
        return Imaging(
            at=self.at.isoformat(),
            name=self.imaging,
            value=self.result,
            link=self.link,
        )
