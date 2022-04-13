from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class DataQuery(object):

    def __init__(self):
        self._engine = create_engine(
            'mssql+pyodbc://sa:Password123@chameleon-db:1433/chameleon_db?driver=ODBC+Driver+18+for+SQL+Server&trustServerCertificate=yes')

    def execute(self, statement):
        with Session(self._engine) as session:
            return session.execute(statement)

    def select(self, statement):
        with Session(self._engine) as session:
            return session.execute(statement).scalars().all()
