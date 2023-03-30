from pydantic import BaseModel
from enum import Enum

from common.data_models.image import ImagingTypes

modality_type_mapping = {
    "DX": ImagingTypes.xray,
    "CT": ImagingTypes.ct,
    "MR": ImagingTypes.mri,
    "US": ImagingTypes.ultrasound,
    "CR": ImagingTypes.xray

}


class RisImaging(BaseModel):
    order_number: str
    imaging_type: ImagingTypes
    sps_code: str
    accession_number: str
