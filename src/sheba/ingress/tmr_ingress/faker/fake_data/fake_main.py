from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .cameleon_main_inserter import ChameleonMainInserter
from .measurements_inserter import MeasurementsInserter

class FakeMain:

    CONNECTION_STRING = 'mssql+pyodbc://sa:Password123@127.0.0.1:1433/chameleon_db?driver=ODBC+Driver+17+for+SQL+Server'

    def __init__(self):
        self.engine = create_engine(FakeMain.CONNECTION_STRING)
        # session = sessionmaker(self.engine)
        self._session = Session(bind=self.engine)
        self.chameleon_inserter = ChameleonMainInserter(self._session)
        self.measurments_inserter = MeasurementsInserter(self._session)

    def run(self):
        self.chameleon_inserter.generate_object()
        self.chameleon_inserter.add_rows()
        self._session.commit()
        self.measurments_inserter.generate_object()
        self.measurments_inserter.add_rows()