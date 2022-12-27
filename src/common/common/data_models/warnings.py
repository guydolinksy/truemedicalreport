from pydantic import BaseModel

from common.data_models.severity import Severity


class PatientWarning(BaseModel):
    content: str
    severity: Severity
    acknowledge: bool = False
