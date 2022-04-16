from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.orm import declarative_base

from tmr_common.data_models.patient import Patient, Admission

Base = declarative_base()


class ChameleonMain(Base):
    __tablename__ = "chameleon_main"

    id_num = Column("id_num", VARCHAR(200), primary_key=True, autoincrement=False)
    patient_id = Column("patient_id", Integer())
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
            identification=self.patient_id,
            name=self.patient_name,
            complaint=self.main_cause,
            admission=Admission(department=self.unit, wing=self.unit_wing, bed=self.bed_num),
            warnings=[],
            severity=self.esi
        )
