from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from ...models.chameleon_main import ChameleonMain


class DataInserterBase:

    def __init__(self, session: Session):
        self.faker = Faker()
        self.faked_objects = []
        self.session = session

    def generate_object(self):
        pass

    def add_rows(self):
        self.session.add_all(self.faked_objects)
        self.session.commit()

    def delete_row(self, user_id):
        pass

    def update_row_by_id(self, table_name, column_name, id, new_value):
        self.session.query(table_name).filter().update({})
        query = update(table_name).where(column_name.c.id_num == id).values({table_name.column_name: new_value})
        self.session.commit()

    def select_inner_patient_id(self):
        query = select(ChameleonMain.Id_Num)
        result = self.session.execute(query).fetchall()
        id_list = [item[0] for item in result]
        return id_list
