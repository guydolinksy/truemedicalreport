from sqlalchemy.orm import Session
from sqlalchemy import select


class DataQuery(object):

    def __init__(self, session: Session):
        self._session = session

    def execute_query(self, statement):
        result = self._session.execute(statement)
        return result