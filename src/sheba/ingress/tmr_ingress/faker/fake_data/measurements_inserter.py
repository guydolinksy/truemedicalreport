from datetime import datetime
import random
from tmr_ingress.faker.fake_data.data_inserter_base import DataInserterBase
from tmr_ingress.models.measurements import Measurements

class MeasurementsInserter(DataInserterBase):

    def __init__(self, session):
        super().__init__(session)

    def generate_object(self):
        measurements_object = Measurements()
        measurements_object.Id_Num = self.faker.pystr_format('?#?###???#?#?#?###?')
        measurements_object.Parameter_Date = (datetime.now().utcnow()).strftime("%Y-%m-%d %H:%M:%S")
        measurements_object.Parameter_ID = random.choice([101, 102, 11, 12])
        measurements_object.Parameter_Name = random.choice(['טמפ', 'דופק', 'לחץ דם סיסטולי', 'לחץ דם דיאסטולי'])
        measurements_object.Result = self.faker.pyfloat(min_value=10, max_value=160, right_digits=2)
        measurements_object.Min_Value = self.faker.pyfloat(min_value=30, max_value=80, right_digits=2)
        measurements_object.Max_Value = self.faker.pyfloat(min_value=80, max_value=150, right_digits=2)
        measurements_object.Warnings = self.faker.sentence()
        self.faked_objects.append(measurements_object)
