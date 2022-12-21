from typing import List

from pydantic import BaseModel

from common.data_models.wing import WingSummary


class Department(BaseModel):
    wings: List[WingSummary]

    class Config:
        orm_mode = True
