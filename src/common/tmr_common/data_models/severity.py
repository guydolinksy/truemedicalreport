from pydantic import BaseModel


class Severity(BaseModel):
    value: int
    at: str
