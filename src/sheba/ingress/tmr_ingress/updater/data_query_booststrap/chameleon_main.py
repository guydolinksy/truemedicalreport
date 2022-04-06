from data_query import DataQuery
from sqlalchemy import select
from ...models.cameleon_main import Patients
STATEMENT = select(Patients)


class ChameleonMainQuery(object):

    def __init__(self, data_query: DataQuery):
        self._data_query = data_query

    def get_chameleon_measurements(self):
        return self._data_query.execute_query(STATEMENT)
