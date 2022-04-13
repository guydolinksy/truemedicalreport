from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fake_data.cameleon_main_inserter import ChameleonMainInserter
from fake_data.measurements_inserter import MeasurementsInserter


class FakeMain:

    CONNECTION_STRING = 'mssql+pyodbc://sa:Password123@127.0.0.1:1433/chameleon_db?driver=ODBC+Driver+17+for+SQL+Server'

    def __init__(self):
        self.engine = create_engine(FakeMain.CONNECTION_STRING)
        self._session = Session(bind=self.engine)
        self.chameleon_inserter = ChameleonMainInserter(self._session)
        self.measurments_inserter = MeasurementsInserter(self._session)

    def insert_new_patient(self):
        inner_patient_id = self.chameleon_inserter.generate_object()
        self.chameleon_inserter.add_rows()
        self._session.commit()
        self.measurments_inserter.generate_all_measurements(inner_patient_id)
        self.measurments_inserter.add_rows()

    def update_measurments(self):
        self.measurments_inserter.update_measurement()
        self.measurments_inserter.add_rows()





main = FakeMain()
main.insert_new_patient()
