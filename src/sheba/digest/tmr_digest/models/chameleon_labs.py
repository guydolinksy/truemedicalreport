import pytz
from sqlalchemy import Float, VARCHAR, Integer, Column, DateTime
from sqlalchemy.orm import declarative_base

from tmr_common.data_models.labs import Laboratory, LabStatus, CategoriesInHebrew

Base = declarative_base()


class ChameleonLabs(Base):
    __tablename__ = "lab_results"
    __table_args__ = {"schema": "dw"}

    patient_id = Column("id", Integer(), primary_key=True)
    order_date = Column("OrderDate", DateTime(), primary_key=True)
    test_type_id = Column("TestCode", Integer(), primary_key=True)
    test_type_name = Column("TestName", VARCHAR(100))
    result = Column("result", VARCHAR(100))
    min_warn_bar = Column("NormMinimum", Float())
    max_warn_bar = Column("NormMaximum", Float())
    collection_date = Column("collectiondate", DateTime())
    result_time = Column("ResultTime", DateTime())

    def to_initial_dal(self):
        return Laboratory(
            patient_id = self.patient_id,
            external_id=f'{self.patient_id}#{self.order_date.astimezone(pytz.UTC).isoformat()}#{self.test_type_id}',
            at=self.order_date.astimezone(pytz.UTC).isoformat(),
            test_type_id=self.test_type_id,
            test_type_name=self.test_type_name,
            category_id=int(str(self.test_type_id)[0:4]),
            category_name=CategoriesInHebrew[int(str(self.test_type_id)[0:4])],
            test_tube_id=9,
            panic_min_warn_bar=None,
            min_warn_bar=self.min_warn_bar,
            max_warn_bar=self.max_warn_bar,
            panic_max_warn_bar=None,
            status=(LabStatus.ordered if self.collection_date is None else
                    LabStatus.collected if self.result_time is None else
                    LabStatus.analyzed)
        )
