from enum import Enum

from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base
from tmr_common.data_models.imaging import Imaging
from tmr_common.data_models.labs import Labs

Base = declarative_base()


class ChameleonLabs(Base):
    __tablename__ = "lab_results"

    patient_id = Column("id", int(), primary_key=True)
    category_id = Column("TestCode", Integer(), primary_key=True)
    test_type_name = Column("TestName", VARCHAR(100))
    result = Column("result", VARCHAR(100))
    min_warn_bar = Column("NormMinimum", float())
    max_warn_bar = Column("NormMaximum", float())
    at = Column("OrderDate", DateTime(), primary_key=True)
    collection_date = Column("ResultTime", DateTime())
    result_time = Column("ResultTime", DateTime())

    def to_initial_dal(self):
        return Labs(
            patient_id=self.patient_id,
            test_tube_id=self.test_tube_id,
            category_id=str(self.category_id)[0:4],
            category_name=None,
            test_type_name=self.test_type_name,
            min_warn_bar=self.min_warn_bar,
            panic_min_warn_bar=None,
            max_warn_bar=self.max_warn_bar,
            at=self.at,
            status="הוזמן" if self.collection_date is None else
            "בעבודה" if self.result_time is None else
            "תוצאות"
        )
