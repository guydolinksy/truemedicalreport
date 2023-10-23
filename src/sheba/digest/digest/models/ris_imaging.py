from pydantic import computed_field

from common.data_models.base import Diffable
from common.data_models.image import ImagingTypes

modality_type_mapping = {
    "DX": ImagingTypes.xray,
    "CT": ImagingTypes.ct,
    "MR": ImagingTypes.mri,
    "US": ImagingTypes.ultrasound,
    "CR": ImagingTypes.xray

}


class RisImaging(Diffable):
    order_number: str
    imaging_type: ImagingTypes
    sps_code: str
    accession_number: str

    @computed_field
    @property
    def external_id(self) -> str:
        return self.accession_number