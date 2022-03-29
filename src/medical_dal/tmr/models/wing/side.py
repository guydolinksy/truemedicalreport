from pydantic import BaseModel


class Side(BaseModel):
    name: str
    beds: list[str]

