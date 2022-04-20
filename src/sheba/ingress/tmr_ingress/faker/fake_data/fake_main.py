import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .chameleon_main_inserter import ChameleonMainInserter
from .measurements_inserter import MeasurementsInserter


class FakeMain(object):
    def __init__(self, connection_string=None):
        connection_string = connection_string or os.getenv('CHAMELEON_CONNECTION_STRING')
        self.engine = create_engine(connection_string)
        self._session = Session(bind=self.engine)
        self.chameleon_inserter = ChameleonMainInserter(self._session)
        self.measurements_inserter = MeasurementsInserter(self._session)

    def insert_new_patient(self):
        inner_patient_id = self.chameleon_inserter.generate_object()
        self.chameleon_inserter.add_rows()
        self.measurements_inserter.generate_all_measurements_for_single_patient(inner_patient_id)
        self.measurements_inserter.add_rows()

    def insert_new_measurements(self):
        self.measurements_inserter.insert_fake_measurements_for_all_patient()
        self.measurements_inserter.add_rows()
