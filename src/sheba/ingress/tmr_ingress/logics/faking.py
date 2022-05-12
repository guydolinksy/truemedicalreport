import contextlib
import copy
import datetime
import os
import random
import requests
import logbook
import pytz
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tmr_common.data_models.labs import LabsCategories, LabTestType, CategoriesInHebrew
from tmr_ingress.models.chameleon_main import ChameleonMain, Departments
from tmr_ingress.models.chameleonimaging import ChameleonImaging
from tmr_common.data_models.imaging import ImagingTypes, ImagingStatus
from tmr_ingress.models.labs import ChameleonLabs
from tmr_ingress.models.measurements import Measurements
from tmr_common.data_models.notification import NotificationLevel, NotificationType, Notification

logger = logbook.Logger(__name__)


class FakeMain(object):
    def __init__(self, connection_string=None):
        connection_string = connection_string or os.getenv('CHAMELEON_CONNECTION_STRING')
        self._engine = create_engine(connection_string)
        self.faker: Faker = Faker('he-IL')

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

    def get_used_beds(self, wing):
        with self.session() as session:
            return {str(cm.bed_num) for cm in (session.query(ChameleonMain).filter(
                (ChameleonMain.unit_wing == wing) & (ChameleonMain.bed_num != None)))}

    def _admit_patient(self, department: Departments, wing):
        o = ChameleonMain()
        o.patient_id = f'{self.faker.pyint(min_value=000000000, max_value=999999999):09}'
        o.gender = 'M' if random.randint(0, 1) else 'F'
        if o.gender == 'M':
            o.patient_name = self.faker.name_male()
        elif o.gender == 'F':
            o.patient_name = self.faker.name_female()

        dob = datetime.datetime.combine(self.faker.date_of_birth(), datetime.time()).astimezone(pytz.UTC)
        if random.randint(0, 100) > 5:
            now = datetime.datetime.utcnow().astimezone(pytz.UTC)
            o.age = f"{int((now - dob).days / 365)}.{int(((now - dob).days % 365) / 30)}"
            if random.randint(0, 100) > 5:
                o.birthdate = dob

        o.unit = int(department.value)
        o.unit_wing = wing
        o.bed_num = random.choice(list(self.wings[wing] - self.get_used_beds(wing)))
        o.arrival = self.faker.past_datetime('-30m').astimezone(pytz.UTC)

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
            result = {patient.chameleon_id for patient in session.query(ChameleonMain).filter(
                (ChameleonMain.unit == int(department.value)) & (ChameleonMain.unit_wing == wing)
            )}
            return result

    def _generate_measurements(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 20)]
        else:
            raise ValueError()
        for patient in patients:
            pulse = Measurements()
            pulse.patient_id = patient
            pulse.at = datetime.datetime.utcnow()
            pulse.code = 12
            pulse.name = 'דופק'
            pulse.min_limit = self.faker.pyint(min_value=55, max_value=65)
            pulse.max_limit = self.faker.pyint(min_value=95, max_value=110)
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                pulse.value = self.faker.pyint(min_value=20, max_value=50)
            elif 4 <= prob < 11:
                pulse.value = self.faker.pyint(min_value=50, max_value=pulse.min_limit)
            elif 11 <= prob < 91:
                pulse.value = self.faker.pyint(min_value=pulse.min_limit, max_value=pulse.max_limit)
            elif 91 <= prob < 98:
                pulse.value = self.faker.pyint(min_value=pulse.max_limit, max_value=115)
            elif 98 <= prob < 101:
                pulse.value = self.faker.pyint(min_value=120, max_value=160)
            pulse.warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.add(pulse)
                session.commit()

            saturation = Measurements()
            saturation.patient_id = patient
            saturation.at = datetime.datetime.utcnow()
            saturation.code = 13
            saturation.name = 'סטורציה'
            saturation.min_limit = self.faker.pyint(min_value=87, max_value=93)
            saturation.max_limit = 100
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                saturation.value = self.faker.pyint(min_value=75, max_value=85)
            elif 4 <= prob < 11:
                saturation.value = self.faker.pyint(min_value=85, max_value=saturation.min_limit)
            elif 11 <= prob < 101:
                saturation.value = self.faker.pyint(min_value=saturation.min_limit, max_value=100)
            saturation.warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.add(saturation)
                session.commit()

            temperature = Measurements()
            temperature.patient_id = patient
            temperature.at = datetime.datetime.utcnow()
            temperature.code = 11
            temperature.name = 'טמפ'
            temperature.min_limit = self.faker.pyint(min_value=356, max_value=361) / 10.
            temperature.max_limit = self.faker.pyint(min_value=377, max_value=380) / 10.
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                temperature.value = self.faker.pyint(min_value=350, max_value=355) / 10.
            elif 4 <= prob < 11:
                temperature.value = self.faker.pyint(min_value=355, max_value=temperature.min_limit * 10) / 10.
            elif 11 <= prob < 91:
                temperature.value = self.faker.pyint(min_value=temperature.min_limit * 10,
                                                     max_value=temperature.max_limit * 10) / 10.
            elif 91 <= prob < 98:
                temperature.value = self.faker.pyint(min_value=temperature.max_limit * 10, max_value=410) / 10.
            elif 98 <= prob < 101:
                temperature.value = self.faker.pyint(min_value=410, max_value=425) / 10.

            with self.session() as session:
                session.add(temperature)
                session.commit()
            systolic, diastolic = Measurements(), Measurements()
            systolic.patient_id = diastolic.patient_id = patient
            systolic.at = diastolic.at = datetime.datetime.utcnow()
            systolic.code, diastolic.code = 101, 102
            systolic.name, diastolic.name = 'לחץ דם סיסטולי', 'לחץ דם דיאסטולי'
            systolic.min_limit = self.faker.pyfloat(min_value=90 * 0.9, max_value=90 * 1.1, right_digits=0)
            systolic.max_limit = self.faker.pyfloat(min_value=120 * 0.9, max_value=120 * 1.1, right_digits=0)
            diastolic.min_limit = self.faker.pyfloat(min_value=60 * 0.9, max_value=60 * 1.1, right_digits=0)
            diastolic.max_limit = self.faker.pyfloat(min_value=90 * 0.9, max_value=90 * 1.1, right_digits=0)
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                systolic.value = self.faker.pyint(min_value=63, max_value=70)
            elif 4 <= prob < 11:
                systolic.value = self.faker.pyint(min_value=70, max_value=int(systolic.min_limit))
            elif 11 <= prob < 91:
                systolic.value = self.faker.pyint(min_value=int(systolic.min_limit),
                                                  max_value=int(systolic.max_limit))
            elif 91 <= prob < 98:
                systolic.value = self.faker.pyint(min_value=int(systolic.max_limit), max_value=210)
            elif 98 <= prob < 101:
                systolic.value = self.faker.pyint(min_value=210, max_value=231)
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                diastolic.value = self.faker.pyint(min_value=min(36, int(systolic.value - 10)),
                                                   max_value=min(40, int(systolic.value - 10)))
            elif 4 <= prob < 11:
                diastolic.value = self.faker.pyint(min_value=min(40, int(systolic.value - 10)),
                                                   max_value=min(int(diastolic.min_limit),
                                                                 int(systolic.value - 10)))
            elif 11 <= prob < 91:
                diastolic.value = self.faker.pyint(
                    min_value=min(int(diastolic.min_limit), int(systolic.value - 10)),
                    max_value=min(int(diastolic.max_limit), int(systolic.value - 10)))
            elif 91 <= prob < 98:
                diastolic.value = self.faker.pyint(
                    min_value=min(int(diastolic.max_limit), int(systolic.value - 10)),
                    max_value=min(130, int(systolic.value - 10)))
            elif 98 <= prob < 101:
                diastolic.value = self.faker.pyint(min_value=min(130, int(systolic.value - 10)),
                                                   max_value=min(143, int(systolic.value - 10)))

            systolic.warnings = self.faker.sentence(nb_words=3)
            diastolic.warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.add(systolic)
                session.add(diastolic)
                session.commit()

    def _generate_imagings(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 20)]
        else:
            raise ValueError()
        for patient in patients:
            im = ChameleonImaging()
            im.patient_id = patient
            im.at = datetime.datetime.utcnow()
            im.type_ = random.choice(list(ImagingTypes)).value
            type_name = {
                ImagingTypes.ct.value: 'CT',
                ImagingTypes.ultrasound.value: 'אולטרהסאונד',
                ImagingTypes.xray.value: 'צילום'
            }
            location = random.choice(['ראש', 'אגן', 'חזה', 'בטן'])
            im.description = f'{type_name[im.type_]} {location}'
            im.status = random.choice(list(ImagingStatus)).value
            im.level = random.choice(list(NotificationLevel)).value
            im.link = self.faker.url()
            with self.session() as session:
                session.add(im)
                session.commit()

    def _generate_labs(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 20)]
        else:
            raise ValueError()
        for patient in patients:
            lab_result = ChameleonLabs()
            lab_result.patient_id = patient
            category = random.choice(list(LabsCategories))
            lab_result.category_id = category.value
            lab_result.category_name = CategoriesInHebrew[category]
            test_types = LabTestType[category]
            lab_result.test_tube_id = random.randint(1, 3)
            for test_type_id, test_type_name in enumerate(test_types):
                lab_result.test_type_id = test_type_id
                lab_result.test_type_name = test_type_name
                lab_result.result = random.choice(
                    [self.faker.pyfloat(min_value=0.1, max_value=100.0, right_digits=2), None])
                lab_result.min_warn_bar = self.faker.pyfloat(min_value=20.0,
                                                             max_value=40.0, right_digits=2)
                lab_result.panic_min_warn_bar = self.faker.pyfloat(min_value=0.0,
                                                                   max_value=39.9, right_digits=2)
                lab_result.max_warn_bar = self.faker.pyfloat(min_value=80.0,
                                                             max_value=100.0, right_digits=2)
                lab_result.panic_max_warn_bar = self.faker.pyfloat(min_value=100.0,
                                                                   max_value=130.0, right_digits=2)
                lab_result.at = datetime.datetime.utcnow()
                lab_result.row_id = f"{lab_result.patient_id}-{lab_result.category_id}-{lab_result.test_type_id}"
                with self.session() as session:
                    session.add(copy.deepcopy(lab_result))
                    session.commit()


    async def admit_patients(self, department):
        for wing in self.wings:
            if random.randint(0, 1):
                chameleon_id, patient_id = self._admit_patient(department, wing)
                self._generate_measurements(chameleon_id=chameleon_id)

    async def discharge_patient(self, department):
        for wing in self.wings:
            for patient in self._get_patients(department, wing):
                if not random.randint(0, 20):
                    self._discharge_patient(patient)

    async def update_measurements(self, department):
        for wing in self.wings:
            self._generate_measurements(department=department, wing=wing)

    async def update_imagings(self, department):
        for wing in self.wings:
            self._generate_imagings(department=department, wing=wing)

    async def update_labs(self, department):
        for wing in self.wings:
            self._generate_labs(department=department, wing=wing)
