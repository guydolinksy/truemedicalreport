from pydantic import BaseModel

from tmr_common.data_models.severity import Severity


class PatientWarning(BaseModel):
    content: str
    severity: Severity
