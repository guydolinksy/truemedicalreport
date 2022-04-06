from sqlalchemy.orm import Session
from sqlalchemy import select, create_engine


class DataQuery(object):

    def __init__(self, host: str, port: int, username: str, password: str):
        self._engine = create_engine(
            f"mssql+pyodbc://{username}:{password}@{host}:{port}/chameleon_db?driver=ODBC+Driver+17+for+SQL+Server")

    def execute_query(self, statement):
        with self._engine.connect() as connection:
            with Session(bind=connection) as session:
                return session.execute(statement)
