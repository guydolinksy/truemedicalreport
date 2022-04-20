import contextlib
import datetime
import os
import random

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tmr_ingress.models.chameleon_main import ChameleonMain, Departments
from tmr_ingress.models.measurements import Measurements


class FakeMain(object):
    def __init__(self, connection_string=None):
        connection_string = connection_string or os.getenv('CHAMELEON_CONNECTION_STRING')
        self._engine = create_engine(connection_string)
        self.faker = Faker('he-IL')

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    wings = {
        'a': {None},
        'b1': {str(i) for i in range(1, 13)} | {None},
        'b2': {str(i) for i in range(13, 25)} | {None},
        'b3': {str(i) for i in range(25, 41)} | {None},
    }
    measurement_types = {
        11: 'טמפ',
        12: 'דופק',
        101: 'לחץ דם סיסטולי',
        102: 'לחץ דם דיאסטולי',
    }

    def get_used_beds(self, wing):
        with self.session() as session:
            return {cm.bed_num for cm in (session.query(ChameleonMain).filter(
                (ChameleonMain.unit_wing == wing) & (ChameleonMain.bed_num != None)))}

    def _generate_patient(self, wing):
        o = ChameleonMain()
        o.patient_id = f'{self.faker.pyint(min_value=000000000, max_value=999999999):09}'
        o.patient_name = self.faker.name()
        o.gender = 'M' if random.randint(0, 1) == 0 else 'F'
        o.unit = int(Departments.er.value)
        o.unit_wing = wing
        o.bed_num = random.choice(list(self.wings[wing] - self.get_used_beds(wing)))
        o.main_cause = random.choice([
            'קוצר נשימה', 'כאבים בחזה', 'סחרחורות', 'חבלת ראש', 'חבלת פנים', 'חבלה בגפיים',
            'בחילות ו/או הקאות', 'כאב ראש', 'כאב בטן', 'לאחר התעלפות'
        ])
        o.esi = random.choice([1, 2, 3, 4])
        o.warnings = self.faker.sentence(nb_words=3)
        o.stage = "מאושפז"
        with self.session() as session:
            session.add(o)
            session.commit()
            return o.id_num, o.patient_id

    def _generate_measurements(self, patient_id=None):
        if patient_id:
            patients = {patient_id}
        else:
            with self.session() as session:
                patients = {patient.patient_id for patient in session.query(ChameleonMain)}

        for patient in patients:
            for type_id in self.measurement_types:
                o = Measurements()
                o.id_num = patient
                o.at = datetime.datetime.utcnow()
                o.code = type_id
                o.name = self.measurement_types[type_id]
                o.value = self.faker.pyfloat(min_value=10, max_value=160, right_digits=2)
                o.min_limit = self.faker.pyfloat(min_value=30, max_value=80, right_digits=2)
                o.max_limit = self.faker.pyfloat(min_value=80, max_value=150, right_digits=2)
                o.warnings = self.faker.sentence(nb_words=3)
                with self.session() as session:
                    session.add(o)
                    session.commit()

    async def admit_patients(self):
        for wing in self.wings:
            if random.randint(0, 1):
                inner_patient_id, patient_id = self._generate_patient(wing)
                self._generate_measurements(patient_id)

    async def discharge_patient(self):
        for wing in self.wings:
            pass

    async def update_measurements(self):
        self._generate_measurements()
