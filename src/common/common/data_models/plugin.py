from typing import List, Optional

from .base import Diffable
from .patient import Patient
from .person import Person


class PatientInfoPluginRender(Diffable):
    key: str
    title: str
    url: str

class PatientInfoPluginConfig(Diffable):
    key: str
    title: str
    url: str
    api_version: str


    def render(self, **kwargs):
        return PatientInfoPluginRender(
            key=self.key,
            title=self.title.format(**kwargs),
            url=self.url.format(**kwargs),
        )


class PanelPatient(Patient):
    plugins: List[PatientInfoPluginRender] = []



class PatientInfoPluginDataV1(Diffable):
    info: Person
    medical_record: Optional[str] = None

