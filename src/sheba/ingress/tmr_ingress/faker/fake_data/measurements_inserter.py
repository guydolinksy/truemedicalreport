from datetime import datetime
import random
from fake_data.data_inserter_base import DataInserterBase
from models.measurements import Measurements


class MeasurementsInserter(DataInserterBase):

    def __init__(self, session):
        super().__init__(session)
        self.measurement_types = {11: 'טמפ', 12: 'דופק', 101: 'לחץ דם סיסטולי', 102: 'לחץ דם דיאסטולי'}

    def generate_object(self, type_id, inner_patient_id):
        measurements_object = Measurements()
        measurements_object.Id_Num = inner_patient_id
        measurements_object.Parameter_Date = (datetime.now().utcnow()).strftime("%Y-%m-%d %H:%M:%S")
        measurements_object.Parameter_ID = type_id
        measurements_object.Parameter_Name = self.measurement_types[type_id]
        measurements_object.Result = self.faker.pyfloat(min_value=10, max_value=160, right_digits=2)
        measurements_object.Min_Value = self.faker.pyfloat(min_value=30, max_value=80, right_digits=2)
        measurements_object.Max_Value = self.faker.pyfloat(min_value=80, max_value=150, right_digits=2)
        measurements_object.Warnings = self.faker.sentence(nb_words=3)
        self.faked_objects.append(measurements_object)

    def generate_all_measurements(self, inner_patient_id):
        for type_id in self.measurement_types:
            self.generate_object(type_id, inner_patient_id)

    def update_measurement(self):
        inner_patient_id = random.choice(self.select_inner_patient_id('measurments.Id_Num'))
        measure_id = random.choice(self.measurement_types.keys())
        self.generate_object(measure_id, inner_patient_id)

