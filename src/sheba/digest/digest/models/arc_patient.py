import datetime
from enum import Enum
from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, String, VARCHAR, DateTime
from digest.models.base import Base


class Departments(Enum):
    er = '1184000'


class ARCPatient(Base):

    __tablename__ = "patients"
    __table_args__ = {"schema": "ris"}

    patient_id = Column("patient_id", Integer(), primary_key=True)
    first_name = Column("first_name", String(30))
    last_name = Column("last_name", String(30))
    gender = Column("gender", VARCHAR(100))
    birthdate = Column("birth_date", DateTime())

    def to_dal(self):
        age = (datetime.now() - self.birthdate) if self.birthdate else None
        return dict(
            external_id=self.patient_id,
            id_=self.patient_id,
            name=' '.join([self.first_name, self.last_name]),
            gender=self.gender,
            age=f'{int(age.days / 365)}.{int((age.days % 365) / 30)}' if age else None,
            birthdate=self.birthdate.astimezone(pytz.UTC).isoformat() if self.birthdate else None,
        )
