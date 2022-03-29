from pydantic import BaseModel


class PatientCount(BaseModel):
    value: int
    
