import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.orm import declarative_base

from tmr_common.data_models.patient import Patient, Admission
from tmr_common.data_models.severity import Severity
from tmr_common.data_models.esi_score import ESIScore

Base = declarative_base()


class Departments(Enum):
    er = '5'


class ChameleonMain(Base):
    __tablename__ = "chameleon_main"

    id_num = Column("id_num", Integer(), primary_key=True)
    patient_id = Column("patient_id", VARCHAR(200))
    patient_name = Column("patient_name", String(30))
    gender = Column("gender", VARCHAR(100))
    unit = Column("unit", Integer())
    unit_wing = Column("unit_wing", String())
    main_cause = Column("main_cause", String())
    esi = Column("esi", Integer())
    bed_num = Column("bed_num", Integer())
    warnings = Column("warnings", String())
    stage = Column("stage", VARCHAR(150))

    def to_dal(self) -> Patient:
        return Patient(
            id_=self.id_num,
            name=self.patient_name,
            complaint=self.main_cause,
            admission=Admission(department=Departments(str(self.unit)).name, wing=self.unit_wing, bed=self.bed_num),
            warnings=[],
            esi=ESIScore(value=self.esi, at=datetime.datetime.utcnow().isoformat())
        )
