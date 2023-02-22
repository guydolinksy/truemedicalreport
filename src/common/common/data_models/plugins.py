from typing import Optional

from pydantic import BaseModel

from .patient import Person


class PatientInfoPluginDataV1(BaseModel):
    info: Person = Person()
    medical_record: Optional[str]
