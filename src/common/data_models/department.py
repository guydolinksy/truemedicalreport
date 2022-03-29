from pydantic import BaseModel
from typing import List
from wing.wing import Wing


class Department(BaseModel):
    wings: List[Wing]

    class Config:
        orm_mode = True
