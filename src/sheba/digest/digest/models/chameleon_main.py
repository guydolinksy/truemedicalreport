from enum import Enum

from sqlalchemy import Column, Integer, VARCHAR, DateTime

from digest.models.base import Base


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
