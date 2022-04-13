from sqlalchemy.orm import Session
from fake_data.data_inserter_base import DataInserterBase
from models.chameleon_main import CameleonMain
import random
import uuid
from faker import Faker


class ChameleonMainInserter(DataInserterBase):

    def __init__(self, session):
        super().__init__(session)

    def generate_object(self):
        chameleon_main_object = CameleonMain()
        chameleon_main_object.Id_Num = self.faker.pystr_format('?#?###???#?#?#?###?')
        chameleon_main_object.patient_id = self.faker.pyint(min_value=000000000, max_value=999999999)
        chameleon_main_object.patient_name = self.faker.name()
        chameleon_main_object.gender = 'M' if random.randint(0, 1) == 0 else 'F'
        chameleon_main_object.Unit = self.faker.pyint(min_value=1, max_value=3)
        chameleon_main_object.Unit_wing = self.faker.pyint(min_value=1, max_value=4)
        chameleon_main_object.Main_cause = random.choice(['קשיי נשימה','כאבים בחזה','סחרחורות','פגיעה בראש', 'פציעה בעין', 'חתך ביד', 'הקאות', 'כאבי ראש', 'כאבי בטן' ])
        chameleon_main_object.ESI = random.choice([1, 2, 3, 4])
        chameleon_main_object.bed_num = self.faker.pyint(min_value=0, max_value=8)
        chameleon_main_object.warnings = self.faker.sentence(nb_words=3)
        self.faked_objects.append(chameleon_main_object)
        return chameleon_main_object.Id_Num


