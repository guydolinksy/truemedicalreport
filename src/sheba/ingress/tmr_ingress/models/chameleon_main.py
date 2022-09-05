from enum import Enum

import pytz
from sqlalchemy import Column, Integer, VARCHAR, DateTime

from tmr_common.data_models.esi_score import ESIScore
from tmr_common.data_models.admission import Admission
from tmr_ingress.models.base import Base


class Departments(Enum):
    er = '1184000'


class ChameleonMain(Base):
    __tablename__ = "Emergency_visits"
    __table_args__ = {"schema": "dw"}

    patient_id = Column("id", Integer(), primary_key=True)
    unit = Column("DepartmentName", VARCHAR(200))
    unit_wing = Column("DepartmentWing", VARCHAR(200))
    department_code = Column("DepartmentCode", Integer(), default=1184000)
    arrival = Column("DepartmentAdmission", DateTime())
    discharge_time = Column("DepartmentWingDischarge", DateTime())
    main_cause = Column("MainCause", VARCHAR(200))
    esi = Column("esi", Integer())

    def to_dal(self):
        return dict(
            arrival=self.arrival.astimezone(pytz.UTC).isoformat(),
            complaint=self.main_cause,
            admission=Admission(department=self.unit, wing=self.unit_wing).dict(),
            esi=ESIScore(value=self.esi, at=self.arrival.astimezone(pytz.UTC).isoformat()).dict(),
            discharge_time=self.discharge_time.astimezone(pytz.UTC).isoformat() if self.discharge_time else None
        )
