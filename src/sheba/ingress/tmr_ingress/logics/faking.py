import contextlib
import datetime
import os
import random

import logbook
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tmr_ingress.models.chameleon_main import ChameleonMain, Departments
from tmr_ingress.models.measurements import Measurements

logger = logbook.Logger(__name__)


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
        "temperature": {"min": 36.1,
                        "max": 37.7,
                        "min_fake": 35.6,
                        "max_fake": 41,
                        "description": 'טמפ',
                        "decimal_digits": 1,
                        "code": 11},
        "pulse": {"min": 50,
                  "max": 110,
                  "min_fake": 35,
                  "max_fake": 210,
                  "description": 'דופק',
                  "decimal_digits": 0,
                  "code": 12},
        "systolic": {"min": 90,
                     "max": 120,
                     "min_fake": 70,
                     "max_fake": 200,
                     "decimal_digits": 0,
                     "description": 'לחץ דם סיסטולי',
                     "code": 101},
        "diastolic": {"min": 60,
                      "max": 80,
                      "min_fake": 50,
                      "max_fake": 160,
                      "decimal_digits": 0,
                      "description": 'לחץ דם דיאסטולי',
                      "code": 102}
    }

    def get_used_beds(self, wing):
        with self.session() as session:
            return {str(cm.bed_num) for cm in (session.query(ChameleonMain).filter(
                (ChameleonMain.unit_wing == wing) & (ChameleonMain.bed_num != None)))}

    def _admit_patient(self, department: Departments, wing):
        o = ChameleonMain()
        o.patient_id = f'{self.faker.pyint(min_value=000000000, max_value=999999999):09}'
        o.patient_name = self.faker.name()
        o.gender = 'M' if random.randint(0, 1) == 0 else 'F'
        o.unit = int(department.value)
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
            return o.chameleon_id, o.patient_id

    def _discharge_patient(self, chameleon_id):
        with self.session() as session:
            patient = session.query(ChameleonMain).where(ChameleonMain.chameleon_id == chameleon_id).first()
            patient.unit = patient.unit_wing = patient.bed_num = None
            session.commit()

    def _get_patients(self, department: Departments, wing):
        with self.session() as session:
            return {patient.chameleon_id for patient in session.query(ChameleonMain).filter(
                (ChameleonMain.unit == int(department.value)) & (ChameleonMain.unit_wing == wing)
            )}

    def _generate_measurements(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = self._get_patients(department, wing)
        else:
            raise ValueError()
        for patient in patients:
            for measure_type in self.measurement_types:
                o = Measurements()
                o.id_num = patient
                o.at = datetime.datetime.utcnow()
                o.code = self.measurement_types[measure_type]["code"]
                o.name = self.measurement_types[measure_type]["description"]
                o.value = self.faker.pyfloat(min_value=self.measurement_types[measure_type]["min_fake"],
                                             max_value=self.measurement_types[measure_type]["max_fake"],
                                             right_digits=self.measurement_types[measure_type]["decimal_digits"])
                o.min_limit = self.measurement_types[measure_type]["min"]
                o.max_limit = self.measurement_types[measure_type]["max"]
                o.warnings = self.faker.sentence(nb_words=3)
                with self.session() as session:
                    session.add(o)
                    session.commit()

    async def admit_patients(self, department):
        for wing in self.wings:
            if random.randint(0, 1):
                chameleon_id, patient_id = self._admit_patient(department, wing)
                self._generate_measurements(chameleon_id)

    async def discharge_patient(self, department):
        for wing in self.wings:
            for patient in self._get_patients(department, wing):
                if not random.randint(0, 10):
                    self._discharge_patient(patient)

    async def update_measurements(self):
        self._generate_measurements()
