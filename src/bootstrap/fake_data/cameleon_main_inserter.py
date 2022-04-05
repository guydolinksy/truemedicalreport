import uuid

from faker import Faker
from sqlalchemy.orm import Session

from fake_data.data_inserter_base import DataInserterBase
from models.cameleon_main import CameleonMain


class CameleonMainInserter(DataInserterBase):

    def __init__(self, sqlalchemy_session: Session):
        super().__init__(sqlalchemy_session)

    def generate_object(self):
        cameleon_main_object = CameleonMain()
        cameleon_main_object.Id_Num = uuid.uuid4()
        cameleon_main_object.patient = self.faker.pyint()
        cameleon_main_object.name = self.faker.name()
        cameleon_main_object.Unit = self.faker.pyint()
        cameleon_main_object.Unit_wing = self.faker.pyint()
        cameleon_main_object.Main_cause = self.faker.sentence()
        cameleon_main_object.ESI = self.faker.pyint()
        cameleon_main_object.bed = self.faker.pyint()
        cameleon_main_object.warnings = self.faker.sentence()
