from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from tmr_ingress.faker.fake_data.data_inserter_base import DataInserterBase
from tmr_ingress.models.measurements import Measurements


class MeasurementsInserter(DataInserterBase):

    def __init__(self, sqlalchemy_session: Session):
        super().__init__(sqlalchemy_session)

    def generate_object(self):
        measurements_object = Measurements()
        measurements_object.Id_Num = uuid.uuid4()
        measurements_object.Parameter_Date = datetime.now()
        measurements_object.Parameter_Name = self.faker.name()
        measurements_object.Result = self.faker.pyfloat(min=10,max=80)
        measurements_object.Warnings = self.faker.sentence()
        measurements_object.Min = self.faker.pyint(min=30,max=80)
        measurements_object.Max = self.faker.pyint(min=80,max=150)
        measurements_object.Parameter_Id = self.faker.pyint(min=100000, max=999999)
