from data_query import DataQuery
from sqlalchemy import select
from models.cameleon_main import CameleonMain
STATEMENT = select(CameleonMain)


class ChameleonMainQuery(object):

    def __init__(self, data_query: DataQuery):
        self._data_query = data_query

    def get_chameleon_measurements(self):
        reuslt = self._data_query.execute_query(STATEMENT)
        return reuslt
