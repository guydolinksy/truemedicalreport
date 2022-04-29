import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, VARCHAR, DateTime
from sqlalchemy.orm import declarative_base

from tmr_common.data_models.patient import Patient, Admission
from tmr_common.data_models.esi_score import ESIScore
from tmr_ingress.models.base import Base


class Departments(Enum):
    er = '5'


class ChameleonMain(Base):
    __tablename__ = "chameleon_main"

    chameleon_id = Column("id_num", Integer(), primary_key=True)

    patient_id = Column("patient_id", VARCHAR(200))
    patient_name = Column("patient_name", String(30))
    gender = Column("gender", VARCHAR(100))
    age = Column("age", VARCHAR)
    birthdate = Column("birthdate", DateTime())

    unit = Column("unit", Integer())
    unit_wing = Column("unit_wing", String())
    bed_num = Column("bed_num", Integer())
    arrival = Column("arrival", DateTime())

    main_cause = Column("main_cause", String())
    esi = Column("esi", Integer())

    stage = Column("stage", VARCHAR(150))
    warnings = Column("warnings", String())

    def to_dal(self) -> Patient:
        return Patient(
            chameleon_id=self.chameleon_id,
            id_=self.patient_id,
            name=self.patient_name,
            arrival=self.arrival.isoformat() if self.arrival else None,
            complaint=self.main_cause,
            admission=Admission(department=Departments(str(self.unit)).name, wing=self.unit_wing, bed=self.bed_num),
            warnings=[],
            esi=ESIScore(value=self.esi, at=datetime.datetime.utcnow().isoformat()),
            gender=self.gender,
            age=self.age,
            birthdate=self.birthdate.isoformat() if self.birthdate else None,
        )
