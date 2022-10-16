from pydantic import BaseModel


class Event(BaseModel):
    key: str
    content: str
    at: str
