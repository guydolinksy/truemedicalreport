from typing import Any, Dict

from ..fake_data.data_inserter_base import DataInserterBase
from ...models.chameleon_main import ChameleonMain
import random


class ChameleonMainInserter(DataInserterBase):
    wings = {
        'a': {None},
        'b1': {str(i) for i in range(1, 13)} | {None},
        'b2': {str(i) for i in range(13, 25)} | {None},
        'b3': {str(i) for i in range(25, 41)} | {None},
    }

    def __init__(self, session):
        super().__init__(session)

    def get_used_beds(self, wing):
        return {cm.bed_num for cm in self.session.query(ChameleonMain).filter(
            (ChameleonMain.unit_wing == wing) & (ChameleonMain.bed_num != None))}

    def generate_object(self):
        chameleon_main_object = ChameleonMain()
        chameleon_main_object.id_num = self.faker.pystr_format('?#?###???#?#?#?###?')
        chameleon_main_object.patient_id = f'{self.faker.pyint(min_value=000000000, max_value=999999999):09}'
        chameleon_main_object.patient_name = self.faker.name()
        chameleon_main_object.gender = 'M' if random.randint(0, 1) == 0 else 'F'
        chameleon_main_object.unit = 5  # self.faker.pyint(min_value=1, max_value=3)
        wing = random.choice(list(self.wings))
        chameleon_main_object.unit_wing = wing
        chameleon_main_object.bed_num = random.choice(list(self.wings[wing] - self.get_used_beds(wing)))
        chameleon_main_object.main_cause = random.choice([
            'קוצר נשימה', 'כאבים בחזה', 'סחרחורות', 'חבלת ראש', 'חבלת פנים', 'חבלה בגפיים',
            'בחילות ו/או הקאות', 'כאב ראש', 'כאב בטן', 'לאחר התעלפות'
        ])
        chameleon_main_object.esi = random.choice([1, 2, 3, 4])
        chameleon_main_object.warnings = self.faker.sentence(nb_words=3)
        chameleon_main_object.stage = "מאושפז"
        self.faked_objects.append(chameleon_main_object)
        return chameleon_main_object.id_num

    def space_chek(self):
        pass

    def release_update(self):
        # inner_patient_id = random.choice(self.select_inner_patient_id())
        # update_row_by_id(self, table_name, column_name, id, new_value)
        pass
