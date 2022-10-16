import pytz
from sqlalchemy import VARCHAR, Integer, Column, DateTime

from common.data_models.image import Image, ImagingStatus
from common.data_models.notification import NotificationLevel
from .base import Base


class ChameleonImaging(Base):
    __tablename__ = "Imaging"
    __table_args__ = {"schema": "dw"}

    imaging_id = Column("sps_key", Integer(), primary_key=True)
    patient_id = Column("ID", Integer())
    order_date = Column("OrderDate", DateTime())
    description = Column("OrderedProcedureType", VARCHAR(100))
    status = Column("ProcedureStatus", VARCHAR(100))
    interpretation = Column("Interpretation", VARCHAR(400))

    def to_dal(self):
        return Image(
            external_id=self.imaging_id,
            patient_id=self.patient_id,
            at=self.order_date.astimezone(pytz.UTC).isoformat(),
            title=self.description,
            status=ImagingStatus(self.status),
            interpretation=self.interpretation,
            level=NotificationLevel.normal,
            link='https://localhost/',
        )
