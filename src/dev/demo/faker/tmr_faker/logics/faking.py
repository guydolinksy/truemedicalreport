import contextlib
import copy
import datetime
import random

import logbook
import pytz
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.data_models.image import ImagingTypes, ImagingStatus
from common.data_models.labs import LabCategories, LabTestType, CategoriesInHebrew
from common.data_models.notification import NotificationLevel
# from digest.models.arc_patient import ARCPatient
# from digest.models.chameleon_imaging import ChameleonImaging
# from digest.models.chameleon_labs import ChameleonLabs
# from digest.models.chameleon_main import ChameleonMain, Departments
# from digest.models.chameleon_measurements import ChameleonMeasurements
# from digest.models.chameleon_medical_free_text import ChameleonMedicalText, FreeTextCodes, Units
from .. import config
from ..utils import sql_statements

logger = logbook.Logger(__name__)


class FakeMain(object):
    def __init__(self, chameleon_connection=None):
        chameleon_connection = chameleon_connection or config.chameleon_connection
        connect_args = {'autocommit': True}
        self._engine = create_engine(chameleon_connection, connect_args=connect_args)
        self.faker: Faker = Faker('he-IL')

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    wings = {'אגף B1', 'אגף B2', 'אגף B3', 'אגף הולכים', 'חדר הלם'}
    department = {'Name': 'המחלקה לרפואה דחופה', 'id': '1184000'}

    def _admit_patient(self, department, wing):
        patient_id = f'{self.faker.pyint(min_value=1, max_value=999999999)}'
        patient_id = patient_id
        gender = 'M' if random.randint(0, 1) else 'F'
        if gender == 'M':
            first_name, last_name = self.faker.last_name_male(), self.faker.first_name_male()
        elif gender == 'F':
            first_name, last_name = self.faker.last_name_female(), self.faker.first_name_female()
        if random.randint(0, 100) > 5:
            birthdate = datetime.datetime.combine(self.faker.date_of_birth(), datetime.time()).astimezone(pytz.UTC)
        arrival = self.faker.past_datetime('-30m').astimezone(pytz.UTC)
        main_cause = random.choice([
            'קוצר נשימה', 'כאבים בחזה', 'סחרחורות', 'חבלת ראש', 'חבלת פנים', 'חבלה בגפיים',
            'בחילות ו/או הקאות', 'כאב ראש', 'כאב בטן', 'לאחר התעלפות'
        ])
        esi = random.choice([1, 2, 3, 4])

        with self.session() as session:
            session.execute(sql_statements.insert_admit_patient.format(ev_MedicalRecord=patient_id, Gender=gender,
                                                                       First_Name=first_name, Last_Name=last_name,
                                                                       Birth_Date=birthdate,
                                                                       UnitName=department["Name"],
                                                                       Wing=wing, Admission_Date=arrival,
                                                                       MainCause=main_cause, ESI=esi))
            session.commit()
        return patient_id

    def _discharge_patient(self, chameleon_id):
        with self.session() as session:
            session.execute(sql_statements.update_discharge_patient.format(ev_MedicalRecord=chameleon_id))
            session.commit()

    def _get_patients(self, department, wing):
        with self.session() as session:
            result = [i[0] for i in session.execute(sql_statements.select_patients_list. \
                                                    format(UnitName=department["Name"], unit_wing=wing))]
            return result

    def _generate_measurements(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 20)]
        else:
            raise ValueError()
        for patient in patients:
            patient_id = patient
            at = datetime.datetime.utcnow()
            code = 61
            name = 'כאב'
            min_limit = 0
            max_limit = 5
            prob = random.randint(1, 100)
            if 1 <= prob < 91:
                m_value = self.faker.pyint(min_value=min_limit, max_value=max_limit)
            elif 91 <= prob < 98:
                m_value = self.faker.pyint(min_value=max_limit, max_value=8)
            elif 98 <= prob < 101:
                m_value = self.faker.pyint(min_value=8, max_value=10)
            # pain.warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.execute(sql_statements.insert_measurements.format(ev_MedicalRecord=patient_id,
                                                                          Device_monitor_date=at,
                                                                          Device_monitor_Parameter=code,
                                                                          Faker_Name=name,
                                                                          Monitoring_Min_Value=min_limit,
                                                                          Monitoring_Max_Value=max_limit,
                                                                          Device_monitor_result=m_value))
                session.commit()

            patient_id = patient
            at = datetime.datetime.utcnow()
            code = 3
            name = 'דופק'
            min_limit = self.faker.pyint(min_value=55, max_value=65)
            max_limit = self.faker.pyint(min_value=95, max_value=110)
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                m_value = self.faker.pyint(min_value=20, max_value=50)
            elif 4 <= prob < 11:
                m_value = self.faker.pyint(min_value=50, max_value=min_limit)
            elif 11 <= prob < 91:
                m_value = self.faker.pyint(min_value=min_limit, max_value=max_limit)
            elif 91 <= prob < 98:
                m_value = self.faker.pyint(min_value=max_limit, max_value=115)
            elif 98 <= prob < 101:
                m_value = self.faker.pyint(min_value=120, max_value=160)
            # warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.execute(sql_statements.insert_measurements.format(ev_MedicalRecord=patient_id,
                                                                          Device_monitor_date=at,
                                                                          Device_monitor_Parameter=code,
                                                                          Faker_Name=name,
                                                                          Monitoring_Min_Value=min_limit,
                                                                          Monitoring_Max_Value=max_limit,
                                                                          Device_monitor_result=m_value))
                session.commit()

            patient_id = patient
            at = datetime.datetime.utcnow()
            code = 13
            name = 'סטורציה'
            min_limit = self.faker.pyint(min_value=87, max_value=93)
            max_limit = 100
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                m_value = self.faker.pyint(min_value=75, max_value=85)
            elif 4 <= prob < 11:
                m_value = self.faker.pyint(min_value=85, max_value=min_limit)
            elif 11 <= prob < 101:
                m_value = self.faker.pyint(min_value=min_limit, max_value=100)
            # warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.execute(sql_statements.insert_measurements.format(ev_MedicalRecord=patient_id,
                                                                          Device_monitor_date=at,
                                                                          Device_monitor_Parameter=code,
                                                                          Faker_Name=name,
                                                                          Monitoring_Min_Value=min_limit,
                                                                          Monitoring_Max_Value=max_limit,
                                                                          Device_monitor_result=m_value))
                session.commit()

            patient_id = patient
            at = datetime.datetime.utcnow()
            code = 1
            name = 'חום'
            min_limit = self.faker.pyint(min_value=356, max_value=361) / 10.
            max_limit = self.faker.pyint(min_value=377, max_value=380) / 10.
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                m_value = self.faker.pyint(min_value=350, max_value=355) / 10.
            elif 4 <= prob < 11:
                m_value = self.faker.pyint(min_value=355, max_value=min_limit * 10) / 10.
            elif 11 <= prob < 91:
                m_value = self.faker.pyint(min_value=min_limit * 10,
                                           max_value=max_limit * 10) / 10.
            elif 91 <= prob < 98:
                m_value = self.faker.pyint(min_value=max_limit * 10, max_value=410) / 10.
            elif 98 <= prob < 101:
                m_value = self.faker.pyint(min_value=410, max_value=425) / 10.

            with self.session() as session:
                session.execute(sql_statements.insert_measurements.format(ev_MedicalRecord=patient_id,
                                                                          Device_monitor_date=at,
                                                                          Device_monitor_Parameter=code,
                                                                          Faker_Name=name,
                                                                          Monitoring_Min_Value=min_limit,
                                                                          Monitoring_Max_Value=max_limit,
                                                                          Device_monitor_result=m_value))
                session.commit()

            systolic_patient_id = diastolic_patient_id = patient
            systolic_at = diastolic_at = datetime.datetime.utcnow()
            systolic_code, diastolic_code = 23, 24
            systolic_name, diastolic_name = 'לחץ סיסטולי', 'לחץ דיאסטולי'
            systolic_min_limit = self.faker.pyfloat(min_value=90 * 0.9, max_value=90 * 1.1, right_digits=0)
            systolic_max_limit = self.faker.pyfloat(min_value=120 * 0.9, max_value=120 * 1.1, right_digits=0)
            diastolic_min_limit = self.faker.pyfloat(min_value=60 * 0.9, max_value=60 * 1.1, right_digits=0)
            diastolic_max_limit = self.faker.pyfloat(min_value=90 * 0.9, max_value=90 * 1.1, right_digits=0)
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                systolic_value = self.faker.pyint(min_value=63, max_value=70)
            elif 4 <= prob < 11:
                systolic_value = self.faker.pyint(min_value=70, max_value=int(systolic_min_limit))
            elif 11 <= prob < 91:
                systolic_value = self.faker.pyint(min_value=int(systolic_min_limit),
                                                  max_value=int(systolic_max_limit))
            elif 91 <= prob < 98:
                systolic_value = self.faker.pyint(min_value=int(systolic_max_limit), max_value=210)
            elif 98 <= prob < 101:
                systolic_value = self.faker.pyint(min_value=210, max_value=231)
            prob = random.randint(1, 100)
            if 1 <= prob < 4:
                diastolic_value = self.faker.pyint(min_value=min(36, int(systolic_value - 10)),
                                                   max_value=min(40, int(systolic_value - 10)))
            elif 4 <= prob < 11:
                diastolic_value = self.faker.pyint(min_value=min(40, int(systolic_value - 10)),
                                                   max_value=min(int(diastolic_min_limit),
                                                                 int(systolic_value - 10)))
            elif 11 <= prob < 91:
                diastolic_value = self.faker.pyint(
                    min_value=min(int(diastolic_min_limit), int(systolic_value - 10)),
                    max_value=min(int(diastolic_max_limit), int(systolic_value - 10)))
            elif 91 <= prob < 98:
                diastolic_value = self.faker.pyint(
                    min_value=min(int(diastolic_max_limit), int(systolic_value - 10)),
                    max_value=min(130, int(systolic_value - 10)))
            elif 98 <= prob < 101:
                diastolic_value = self.faker.pyint(min_value=min(130, int(systolic_value - 10)),
                                                   max_value=min(143, int(systolic_value - 10)))

            # systolic_warnings = self.faker.sentence(nb_words=3)
            # diastolic_warnings = self.faker.sentence(nb_words=3)
            with self.session() as session:
                session.execute(sql_statements.insert_measurements.format(ev_MedicalRecord=systolic_patient_id,
                                                                          Device_monitor_date=systolic_at,
                                                                          Device_monitor_Parameter=systolic_code,
                                                                          Faker_Name=systolic_name,
                                                                          Monitoring_Min_Value=systolic_min_limit,
                                                                          Monitoring_Max_Value=systolic_max_limit,
                                                                          Device_monitor_result=systolic_value))
                session.execute(sql_statements.insert_measurements.format(ev_MedicalRecord=diastolic_patient_id,
                                                                          Device_monitor_date=diastolic_at,
                                                                          Device_monitor_Parameter=diastolic_code,
                                                                          Faker_Name=diastolic_name,
                                                                          Monitoring_Min_Value=diastolic_min_limit,
                                                                          Monitoring_Max_Value=diastolic_max_limit,
                                                                          Device_monitor_result=diastolic_value))
                session.commit()

    def _generate_imagings(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 20)]
        else:
            raise ValueError()
        for patient in patients:
            patient_id = patient
            order_date = datetime.datetime.utcnow()
            type_ = random.choice(list(ImagingTypes)).value
            type_name = {
                ImagingTypes.ct.value: 'CT',
                ImagingTypes.ultrasound.value: 'US',
                ImagingTypes.xray.value: 'צילום'
            }
            location = random.choice(['ראש', 'אגן', 'בית החזה בשכיבה/ישיבה', 'מוח', 'בטן', 'עמוד שדרה'])
            description = f'{type_name[type_]} {location}'
            status = random.choice(list(ImagingStatus)).value
            level = random.choice(list(NotificationLevel)).value
            order_number = random.randint(1000000000000, 9999999999999)
            # link = self.faker.url()
            with self.session() as session:
                session.execute(
                    sql_statements.insert_images.format(ev_MedicalRecord=patient_id, TestOrders_Test_Date=order_date,
                                                        AuxTest_Name=description, TestDates_Panic=level,
                                                        TestOrders_Order_Num=order_number,
                                                        TestOrders_Order_Status=status))
                session.commit()

    def _generate_labs(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 5)]
        else:
            raise ValueError()
        for patient in patients:
            step = random.randint(0, 100)
            if step < 10:
                continue
            category = random.choice(list(LabCategories))
            h_category = CategoriesInHebrew[category]
            order_date = self.faker.date_time_between_dates('-30m', '-10m').astimezone(pytz.UTC)
            collection_date = self.faker.date_time_between_dates('-10m', '-8m').astimezone(pytz.UTC)
            order_number = random.randint(100000000, 999999999)
            for test_type_id, test_type_name in enumerate(LabTestType[category]):
                patient_id = patient
                order_date = order_date
                # test_type_id = f'{category.value}{test_type_id:04}'
                test_type_name = test_type_name
                min_warn_bar = self.faker.pyfloat(min_value=20.0,
                                                  max_value=40.0, right_digits=2)
                panic_min_warn_bar = self.faker.pyfloat(min_value=0.0,
                                                        max_value=39.9, right_digits=2)
                max_warn_bar = self.faker.pyfloat(min_value=80.0,
                                                  max_value=100.0, right_digits=2)
                panic_max_warn_bar = self.faker.pyfloat(min_value=100.0,
                                                        max_value=130.0, right_digits=2)

                if step > 30:
                    collection_date = collection_date
                    if step > 65:
                        if random.randint(0, 1):
                            result_time = self.faker.past_datetime('-8m').astimezone(pytz.UTC)
                            result = self.faker.pyfloat(min_value=0.1, max_value=100.0, right_digits=2)
                with self.session() as session:
                    session.execute(
                        sql_statements.insert_labs.format(ev_MedicalRecord=patient_id, LR_Test_code=order_number,
                                                          Lab_Headline_Name=h_category, LR_Test_Name=test_type_name,
                                                          LR_Result=result, LR_Norm_Minimum=min_warn_bar,
                                                          LR_Norm_Maximum=max_warn_bar, LR_Result_Date=order_date,
                                                          LR_Result_Entry_Date=result_time, LR_Units=None))
                    session.commit()

    def _generate_referrals_dates(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 5)]
        else:
            raise ValueError()
        for patient in patients:
            with self.session() as session:
                session.execute(sql_statements.execute_set_responsible_doctor.format(patient))
                session.commit()

    def _generate_treatment(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 2)]
        else:
            raise ValueError()
        for patient in patients:
            with self.session() as session:
                session.execute(sql_statements.execute_set_hospitalize_or_discharge.format(patient))
                session.commit()

    def _generate_nurse_summary(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 5)]
        else:
            raise ValueError()
        for patient in patients:
            with self.session() as session:
                if session.query(ChameleonMedicalText).filter(
                        (ChameleonMedicalText.patient_id == patient) &
                        (ChameleonMedicalText.medical_text_code == FreeTextCodes.NURSE_SUMMARY.value)
                ).first():
                    continue
            patient_medical_text = ChameleonMedicalText(
                patient_id=patient,
                medical_record=random.randint(0, 500000),
                documenting_date=datetime.date.today(),
                documenting_time=datetime.datetime.utcnow(),
                documenting_user=random.randint(200, 5800),
                unit_name=Units.ER.name,
                unit=Units.ER.value,
                medical_text_code=FreeTextCodes.NURSE_SUMMARY.value,
                medical_text_title=FreeTextCodes.NURSE_SUMMARY.name,
                medical_text=random.choice([
                    """ בדרך כלל בריא, חווה כאבים בצד שמאל מאתמול בערב. מלווה בכאבי ראש וסחרחורות לסירוגין""",
                    """לא מסוגל להזיז את היד, חשש לשבר במפרק כף היד""",
                    """מתלונן על כאבי גב מזה תקופה ארוכה, לטענתו חווה קשיי בעת מעבר בין ישיבה לעמידה""",
                ]),
            )
            with self.session() as session:
                session.add(patient_medical_text)

                session.commit()

    def _generate_doctor_visit(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing) if not random.randint(0, 5)]
        else:
            raise ValueError()
        for patient in patients:
            patient_id = patient,
            documenting_time = datetime.datetime.utcnow(),
            unit = department["id"],
            medical_text = "נבדק"
            with self.session() as session:
                session.execute(
                    sql_statements.update_doctor_visits.format(ev_MedicalRecord=patient_id,
                                                               Doctor_intake_MedicalText=medical_text,
                                                               Doctor_intake_Time=documenting_time, doc_unit=unit))
                session.commit()

    def _generate_room_placements(self, chameleon_id=None, department=None, wing=None):
        if chameleon_id:
            patients = {chameleon_id}
        elif department and wing:
            patients = [p for p in self._get_patients(department, wing)]
        else:
            raise ValueError()
        for patient in patients:
            with self.session() as session:
                session.execute(sql_statements.execute_set_patient_admission.format(patient, random.randint(0, 5)))
                session.commit()

    async def admit_patients(self, department):
        for wing in self.wings:
            if random.randint(0, 1):
                chameleon_id = self._admit_patient(department, wing)
                self._generate_measurements(chameleon_id=chameleon_id)

    async def discharge_patient(self, department):
        for wing in self.wings:
            for patient in self._get_patients(department, wing):
                if not random.randint(0, 3):
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

    async def update_referrals(self, department):
        for wing in self.wings:
            self._generate_referrals_dates(department=department, wing=wing)

    async def update_nurse_summaries(self, department):
        for wing in self.wings:
            self._generate_nurse_summary(department=department, wing=wing)

    async def update_doctor_visits(self, department):
        for wing in self.wings:
            self._generate_doctor_visit(department=department, wing=wing)

    async def update_room_placements(self, department):
        for wing in self.wings:
            self._generate_room_placements(department=department, wing=wing)

    async def update_treatment(self, department):
        for wing in self.wings:
            self._generate_treatment(department=department, wing=wing)

    def clear(self):
        with self.session() as session:
            session.query(ChameleonMain).delete()
            session.query(ARCPatient).delete()
            session.query(ChameleonImaging).delete()
            session.query(ChameleonLabs).delete()
            session.query(ChameleonMeasurements).delete()
            session.query(ChameleonMedicalText).delete()
            session.execute(sql_statements.delete_admission_treatment_decision)
            session.execute(sql_statements.delete_responsible_doctor)
            session.execute(sql_statements.delete_room_placement)
            session.commit()
