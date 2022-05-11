from enum import Enum

from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.labs import Labs

Base = declarative_base()


class ChameleonLabs(Base):
    __tablename__ = "labs"

    row_id = Column("row_id", VARCHAR(200), primary_key=True)
    patient_id = Column("patient_id", VARCHAR(100))
    category_id = Column("category_id", VARCHAR(100))
    category_name = Column("category_name", VARCHAR(100))
    test_type_id = Column("test_type_id", Integer())
    test_tube_id = Column("test_tube_id", VARCHAR)
    test_type_name = Column("test_type_name", VARCHAR(100))
    result = Column("result", VARCHAR(100))
    min_warn_bar = Column("min_warn_bar", Integer())
    panic_min_warn_bar = Column("panic_min_warn_bar", Integer())
    max_warn_bar = Column("max_warn_bar", Integer())
    panic_max_warn_bar = Column("panic_max_warn_bar", Integer())
    at = Column("result_date", DateTime())

    def to_initial_dal(self):
        return Labs(
            patient_id=self.patient_id,
            test_tube_id=self.test_tube_id,
            category_id=self.category_id,
            category_name=self.category_name,
            test_type_id=self.test_type_id,
            test_type_name=self.test_type_name,
            min_warn_bar=self.min_warn_bar,
            panic_min_warn_bar=self.panic_min_warn_bar,
            max_warn_bar=self.max_warn_bar,
            at=self.at,
        )
