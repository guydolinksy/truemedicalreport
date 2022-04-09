from faker import Faker

class DataInserterBase:
    # CONNECTION_STRING = 'mssql+pyodbc://sa:Password123@127.0.0.1:1433'

    def __init__(self, session):
        # self.engine = create_engine(DataInserterBase.CONNECTION_STRING)
        # self._sqlalchemy_session = sessionmaker(self.engine)
        # self._sqlalchemy_session = sqlalchemy_session
        self.faker = Faker()
        self.faked_objects = []
        self.session = session

    def generate_object(self):
        pass

    def add_rows(self):
        # session = Session()
        self.session.add_all(self.faked_objects)
        self.session.commit()
