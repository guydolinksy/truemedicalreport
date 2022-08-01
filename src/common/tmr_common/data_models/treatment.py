from pydantic import BaseModel


class Treatment(BaseModel):
    destination: str
