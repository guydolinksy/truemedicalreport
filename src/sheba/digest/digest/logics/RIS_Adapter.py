import oracledb
from .. import config
from ..utils.sql_statements import query_ris_imaging
from ..models.ris_imaging import RisImaging


class OracleAdapter:
    def __init__(self, username: str, password: str, host: str, service_name: str, port=1521) -> None:
        params = oracledb.ConnectParams(password=password, host=host, port=port, service_name=service_name,
                                        user=username)
        self._conn = oracledb.connect(params=params)

    def query_imaging(self, orders: str):
        with self._conn.cursor() as cursor:
            results = cursor.execute(query_ris_imaging.format(orders))
            return [RisImaging(order_number=result[0], imaging_type=result[1], sps_code=result[2],
                               accession_number=result[3])
                    for result in results]
