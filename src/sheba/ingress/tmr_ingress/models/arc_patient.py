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


class ARCPatient(Base):
    __tablename__ = "patients"

    patient_id = Column("id", Integer(), primary_key=True)
    first_name = Column("first_name", String(30))
    last_name = Column("last_name", String(30))
    gender = Column("gender", VARCHAR(100))
    birthdate = Column("birth_date", DateTime())

    def to_dal(self):
        age = (datetime.now() - self.birthdate) if self.birthdate else None
        return dict(
            external_id=self.patient_id,
            name=' '.join([self.first_name, self.last_name]),
            gender=self.gender,
            age=f'{int(age.days / 365)}.{int((age.days % 365) / 30)}' if age else None,
            birthdate=self.birthdate.isoformat() if self.birthdate else None,
        )
