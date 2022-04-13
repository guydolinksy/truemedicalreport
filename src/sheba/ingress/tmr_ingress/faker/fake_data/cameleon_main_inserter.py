from ..fake_data.data_inserter_base import DataInserterBase
from ...models.cameleon_main import ChameleonMain
import random


class ChameleonMainInserter(DataInserterBase):

    def __init__(self, session):
        super().__init__(session)


    def generate_object(self):
        chameleon_main_object = ChameleonMain()
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
        chameleon_main_object.stage = patient_stage
        self.faked_objects.append(chameleon_main_object)
        return chameleon_main_object.Id_Num

    def space_chek(self):
        pass

    def release_update(self):
        inner_patient_id = random.choice(self.select_inner_patient_id())
        update_row_by_id(self, table_name, column_name, id, new_value)

