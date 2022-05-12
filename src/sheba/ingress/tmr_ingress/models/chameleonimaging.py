from sqlalchemy import VARCHAR, Integer, Column, DateTime
from tmr_common.data_models.imaging import Imaging, ImagingTypes, ImagingStatus
from tmr_common.data_models.notification import NotificationLevel
from .base import Base


class ChameleonImaging(Base):
    __tablename__ = "Imaging"

    imaging_id = Column("sps_key", Integer(), primary_key=True)
    patient_id = Column("ID", int())
    description = Column("OrderedProcedureType", VARCHAR(100))
    status = Column("ProcedureStatus", VARCHAR(100))
    Interpretation = Column("Interpretation", VARCHAR(400))
    order_date = Column("OrderDate", DateTime())


    def to_dal(self):

        return Imaging(
            patient_id=self.patient_id,
            external_id=self.imaging_id,
            at=self.order_date.isoformat(),
            description=self.description,
            status=ImagingStatus(self.status),
            link='https://localhost/'
        )
