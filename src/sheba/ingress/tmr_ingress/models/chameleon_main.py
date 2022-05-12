import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, VARCHAR, DateTime
from sqlalchemy.orm import declarative_base

from tmr_common.data_models.measures import Measures
from tmr_common.data_models.patient import Patient, Admission, ExternalPatient
from tmr_common.data_models.esi_score import ESIScore
from tmr_ingress.models.base import Base


class Departments(Enum):
    er = '5'


class ChameleonMain(Base):
    __tablename__ = "Emergency_visits"

    chameleon_id = Column("id", Integer(), primary_key=True)
    patient_id = Column("patient_id", VARCHAR(200))
    unit = Column("DepartmentName", Integer())
    unit_wing = Column("DepartmentWing", String())
    arrival = Column("DepartmentAdmission", DateTime())
    main_cause = Column("MainCause", String())
    esi = Column("esi", Integer())

    def to_dal(self) -> ExternalPatient:
        return ExternalPatient(
            external_id=self.chameleon_id,
            id_=self.patient_id,
            arrival=self.arrival.isoformat() if self.arrival else None,
            complaint=self.main_cause,
            admission=Admission(department=Departments(str(self.unit)).name, wing=self.unit_wing),
            esi=ESIScore(value=self.esi, at=datetime.datetime.utcnow().isoformat()),
            measures=Measures()
        )

    # def to_dal(self) -> ExternalPatient:
    #     return ExternalPatient(
    #         external_id=self.chameleon_id,
    #         id_=self.patient_id,
    #         name=self.patient_name,
    #         arrival=self.arrival.isoformat() if self.arrival else None,
    #         complaint=self.main_cause,
    #         admission=Admission(department=Departments(str(self.unit)).name, wing=self.unit_wing, bed=self.bed_num),
    #         esi=ESIScore(value=self.esi, at=datetime.datetime.utcnow().isoformat()),
    #         gender=self.gender,
    #         age=self.age,
    #         birthdate=self.birthdate.isoformat() if self.birthdate else None,
    #     )
