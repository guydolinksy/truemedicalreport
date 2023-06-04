import oracledb

from common.data_models.image import ImagingTypes
from ..models.ris_imaging import RisImaging
from ..utils.sql_statements import query_ris_imaging

modality_type_mapping = {
    "DX": ImagingTypes.xray,
    "CT": ImagingTypes.ct,
    "MR": ImagingTypes.mri,
    "US": ImagingTypes.ultrasound,
    "CR": ImagingTypes.xray

}


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
                imaging[str(result[3])] = RisImaging(
                    order_number=result[0],
                    imaging_type=modality_type_mapping.get(result[1], ImagingTypes.unknown),
                    sps_code=result[2],
                    accession_number=result[3]
                )

        return imaging
