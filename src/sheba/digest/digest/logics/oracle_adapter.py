import logbook
import oracledb

from common.data_models.image import ImagingTypes
from ..models.ris_imaging import RisImaging
from ..utils.sql_statements import query_ris_imaging, query_lab_in_progress, RISImagingQuery, LabInProgressQuery

modality_type_mapping = {
    "DX": ImagingTypes.xray,
    "CT": ImagingTypes.ct,
    "MR": ImagingTypes.mri,
    "US": ImagingTypes.ultrasound,
    "CR": ImagingTypes.xray

}
logger = logbook.Logger(__name__)


class OracleAdapter:

    def __init__(self, connection_params) -> None:

        self.params = oracledb.ConnectParams(
            password=connection_params["password"],
            host=connection_params["host"],
            port=connection_params["port"],
            service_name=connection_params["service_name"],
            user=connection_params["username"]
        )

    def query_imaging(self, accessions: list[str]) -> dict[str, RisImaging]:
        imaging = {}
        with oracledb.connect(params=self.params).cursor() as cursor:
            results = cursor.execute(query_ris_imaging.format(', '.join(set(accessions))))
            for result in results:
                i = RisImaging(
                    order_number=str(result[RISImagingQuery.ORDER_KEY]),
                    imaging_type=modality_type_mapping.get(
                        result[RISImagingQuery.MODALITY_TYPE_CODE],
                        ImagingTypes.unknown
                    ),
                    sps_code=result[RISImagingQuery.SPS_CODE],
                    accession_number=str(result[RISImagingQuery.SPS_KEY]),
                )
                imaging[i.external_id] = i
        return imaging

    def query_labs(self, order_numbers: list[str]) -> dict[str, dict]:
        labs = {}
        with oracledb.connect(params=self.params).cursor() as cursor:
            results = cursor.execute(query_lab_in_progress.format(orders="', '".join(set(order_numbers))))
            logger.debug('HERE')
            for result in results:
                labs.setdefault(str(result[LabInProgressQuery.ORDER_NUMBER]), []).append({
                    LabInProgressQuery.TEST_CODE: result[LabInProgressQuery.TEST_CODE],
                    LabInProgressQuery.TEST_NAME: result[LabInProgressQuery.TEST_NAME],
                })

        return labs
