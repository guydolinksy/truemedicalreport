from enum import Enum

from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.labs import LabTest

Base = declarative_base()


class ChameleonLabs(Base):
    __tablename__ = "labs"

    row_id = Column("row_id", VARCHAR(200), primary_key=True)
    patient_id = Column("patient_id", Integer())
    category_id = Column("category_id", VARCHAR(100))
    category_name = Column("category_name", VARCHAR(100))
    test_type_id = Column("test_type_id", Integer())
    test_tube_id = Column("test_tube_id", Integer())
    test_type_name = Column("test_type_name", VARCHAR(100))
    result = Column("result", Float())
    min_warn_bar = Column("min_warn_bar", Float())
    panic_min_warn_bar = Column("panic_min_warn_bar", Float())
    max_warn_bar = Column("max_warn_bar", Float())
    panic_max_warn_bar = Column("panic_max_warn_bar", Float())
    at = Column("result_date", DateTime())

    def to_initial_dal(self) ->LabTest:
        return LabTest(
            patient_id=self.patient_id,
            category_id=self.category_id,
            category_name=self.category_name,
            test_type_id=self.test_type_id,
            test_type_name=self.test_type_name,
            min_warn_bar=self.min_warn_bar,
            panic_min_warn_bar=self.panic_min_warn_bar,
            max_warn_bar=self.max_warn_bar,
            at=self.at,
        )

