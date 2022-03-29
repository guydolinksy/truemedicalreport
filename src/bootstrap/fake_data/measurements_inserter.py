from datetime import datetime

from sqlalchemy.orm import Session

from fake_data.data_inserter_base import DataInserterBase
from models.measurements import Measurements


class MeasurementsInserter(DataInserterBase):

    def __init__(self, sqlalchemy_session: Session):
        super().__init__(sqlalchemy_session)

    def generate_object(self):
        measurements_object = Measurements()
        measurements_object.Id_Num = self.faker.pyint(min=100000, max=999999)
        measurements_object.Parameter_Date = datetime.now()
        measurements_object.Parameter_Name = self.faker.name()
        measurements_object.Result = self.faker.sentence()
        measurements_object.Warnings = self.faker.sentence()
