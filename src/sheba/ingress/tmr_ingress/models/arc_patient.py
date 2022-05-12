import datetime
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, VARCHAR, DateTime
from sqlalchemy.orm import declarative_base

from tmr_common.data_models.measures import Measures
from tmr_common.data_models.patient import Patient, Admission, ExternalPatient
from tmr_common.data_models.esi_score import ESIScore
from tmr_ingress.models.base import Base


class Departments(Enum):
    er = '5'


class ArcPatient(Base):
    __tablename__ = "patients"

    chameleon_id = Column("id", Integer(), primary_key=True)
    patient_id = Column("id", VARCHAR(200))
    patient_first_name = Column("first_name", String(30))
    patient_last_name = Column("last_name", String(30))
    gender = Column("gender", VARCHAR(100))
    birthdate = Column("birth_date", DateTime())

    def to_dal(self) -> ExternalPatient:
        return ExternalPatient(
            external_id=self.chameleon_id,
            id_=self.patient_id,
            name=self.patient_fist_name+' '+self.patient_last_name,
            gender=self.gender,
            age=datetime.now()-self.birthdate,
            birthdate=self.birthdate.isoformat() if self.birthdate else None,
        )
