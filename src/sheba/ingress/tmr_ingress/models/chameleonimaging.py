from sqlalchemy import VARCHAR, Integer, Column, DateTime
from tmr_common.data_models.imaging import Imaging, ImagingTypes, ImagingStatus
from tmr_common.data_models.notification import NotificationLevel
from .base import Base


class ChameleonImaging(Base):
    __tablename__ = "imaging"

    imaging_id = Column("imaging_id", Integer(), primary_key=True)
    patient_id = Column("patient_id", VARCHAR(250))
    type_ = Column("type", VARCHAR(60))
    description = Column("description", VARCHAR(100))
    status = Column("status", VARCHAR(100))
    level = Column("level", Integer())
    link = Column("link", VARCHAR(100))
    at = Column("result_date", DateTime())

    def to_dal(self):

        return Imaging(
            patient_id=self.patient_id,
            external_id=self.imaging_id,
            at=self.at.isoformat(),
            type_=ImagingTypes(self.type_),
            description=self.description,
            status=ImagingStatus(self.status),
            link=self.link,
            level=NotificationLevel(self.level),
        )
