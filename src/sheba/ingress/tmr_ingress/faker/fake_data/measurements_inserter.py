from datetime import datetime
import random
from ..fake_data.data_inserter_base import DataInserterBase
from ...models.measurements import Measurements


class MeasurementsInserter(DataInserterBase):

    def __init__(self, session):
        super().__init__(session)
        self.measurement_types = {
            "temperature": {"min": 36.1,
                            "max": 37.7,
                            "min_fake": 35.6,
                            "max_fake": 41,
                            "description": 'טמפ',
                            "code": 11},
            "pulse": {"min": 50,
                      "max": 110,
                      "min_fake": 35,
                      "max_fake": 210,
                      "description": 'דופק',
                      "code": 12},
            "systolic": {"min": 90,
                         "max": 120,
                         "min_fake": 70,
                         "max_fake": 200,
                         "description": 'לחץ דם סיסטולי',
                         "code": 101},
            "diastolic": {"min": 60,
                          "max": 80,
                          "min_fake": 50,
                          "max_fake": 160,
                          "description": 'לחץ דם דיאסטולי',
                          "code": 102}
        }

    def _fake_measure_value(self, measure_type):
        if measure_type == "temperature":
            value = self.faker.pyfloat(min_value=self.measurement_types[measure_type]["min_fake"],
                                       max_value=self.measurement_types[measure_type]["max_fake"],
                                       right_digits=1)
        else:
            value = self.faker.pyint(min_value=self.measurement_types[measure_type]["min_fake"],
                                     max_value=self.measurement_types[measure_type]["max_fake"])
        return value

    def _fake_single_measure(self, measure_type: str, inner_patient_id: str) -> Measurements:
        measurements_object = Measurements()
        measurements_object.id_num = inner_patient_id
        measurements_object.at = datetime.utcnow()
        measurements_object.code = self.measurement_types[measure_type]["code"]
        measurements_object.name = self.measurement_types[measure_type]["description"]
        measurements_object.warnings = self.faker.sentence(nb_words=3)
        measurements_object.value = self._fake_measure_value(measure_type)
        measurements_object.min_limit = self.measurement_types[measure_type]["min"]
        measurements_object.max_limit = self.measurement_types[measure_type]["max"]
        return measurements_object

    def generate_all_measurements_for_single_patient(self, inner_patient_id):
        for measure_type in self.measurement_types:
            measures = self._fake_single_measure(measure_type, inner_patient_id)
            self.faked_objects.append(measures)

    def insert_fake_measurements_for_all_patient(self):
        patients_id = self.get_patients_id()
        for patient_id in patients_id:
            self.generate_all_measurements_for_single_patient(patient_id)
