from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


class DataInserterBase:

    def __init__(self, session: Session):
        self.faker = Faker()
        self.faked_objects = []
        self.session = session

    def generate_object(self):
        pass

    def add_rows(self):
        # session = Session()
        self.session.add_all(self.faked_objects)
        self.session.commit()

    def delete_row(self, user_id):
        pass

    def update_row(self):
        setattr()

    def select_inner_patient_id(self, select_by):
        query = select(select_by)
        return self.session.execute(query)
