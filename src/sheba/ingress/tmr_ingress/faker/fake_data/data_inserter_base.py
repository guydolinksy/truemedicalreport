from faker import Faker
from sqlalchemy.orm import Session


class DataInserterBase(object):

    def __init__(self, sqlalchemy_session: Session):
        self._sqlalchemy_session = sqlalchemy_session
        self.faker = Faker()
        self.generated_objects = []

    def generate_object(self):
        pass

    def add_rows(self):
        self._sqlalchemy_session.add_all(self.generated_objects)
        self._sqlalchemy_session.commit()
