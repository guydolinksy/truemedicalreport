from pydantic import BaseModel
from typing import Optional


class Medicine(BaseModel):
    label: Optional[str]
    dosage: Optional[str]
    completed: Optional[bool]
    since: Optional[str]

    def get_instance_id(self):
        return f'{self.label}#{self.since.replace(":", "-")}'
