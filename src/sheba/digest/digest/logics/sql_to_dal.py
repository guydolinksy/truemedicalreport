import contextlib
from enum import Enum

import logbook
import pytz
import requests
from requests import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.data_models.admission import Admission
from common.data_models.esi_score import ESIScore
from common.data_models.image import ImagingStatus, Image
from common.data_models.labs import Laboratory, LabStatus, CategoriesInHebrew
from common.data_models.measures import Measure, MeasureType
from common.data_models.notification import NotificationLevel
from common.data_models.patient import Intake, ExternalPatient, Person
from common.data_models.referrals import Referral
from common.data_models.treatment import Treatment
from .. import config
from ..utils import sql_statements, utils

logger = logbook.Logger(__name__)

SHEBA_IMAGING_STATUS = {
    103: ImagingStatus.performed,  # הסתיימה
    106: ImagingStatus.ordered,  # שובץ
    108: ImagingStatus.performed,  # לא פוענח
    109: ImagingStatus.performed,  # לא פוענח
    111: ImagingStatus.analyzed,  # פוענח
    112: ImagingStatus.analyzed,  # הוקלד
    114: ImagingStatus.verified,  # אושרר
    119: ImagingStatus.ordered,  # הפנייה חדשה
    120: ImagingStatus.cancelled,  # בוטל ע"י טכנאי
    122: ImagingStatus.cancelled,  # הפנייה נדחתה
    125: ImagingStatus.ordered,  # הפנייה אושרה
    127: ImagingStatus.analyzed,  # הפנייה לאישור
}

SHEBA_IMAGING_LEVEL = {
    0: NotificationLevel.normal,
    1: NotificationLevel.panic,
}


class SqlToDal(object):
    def __init__(self, chameleon_connection=None, dal_url=None):
        self.dal_url = dal_url or config.dal_url

        chameleon_connection = chameleon_connection or config.chameleon_connection
        self._engine = create_engine(chameleon_connection)

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    def update_admissions(self, department: Departments):
        try:
            logger.debug('Getting admissions for `{}`...', department.name)

            patients = []
            with self.session() as session:
                for row in session.execute(sql_statements.query_patient_admission.format(unit=department.value)):
                    patients.append(ExternalPatient(
                        external_id=row["MedicalRecord"],
                        info=Person(
                            id_=row["MedicalRecord"],
                            name=row["FullName"],
                            gender='male' if row["Gender"] == 'זכר' else 'female',
                            birthdate=utils.datetime_utc_serializer(row["BirthDate"]),
                            age=utils.calculate_patient_age(row["BirthDate"]),
                        ),
                        esi=ESIScore(
                            value=row["ESI"],
                            at=utils.datetime_utc_serializer(row["AdmissionDate"]),
                        ),
                        admission=Admission(
                            department=department.name,
                            wing=row["RoomName"],
                            bed=row["BedName"],
                            arrival=utils.datetime_utc_serializer(row["AdmissionDate"]),
                        ),
                        intake=Intake(
                            complaint=row["MainCause"],
                        ),
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/admissions',
                                json={'admissions': patients})
            res.raise_for_status()

        except HTTPError:
            logger.exception('Could not run admissions handler.')

    def update_measurements(self, department: Departments):
        try:
            logger.debug('Getting measurements for `{}`...', department.name)

            measures = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_measurements.format(
                        unit=department.value, codes='({})'.format(','.join(map(str, sheba_measurement_codes)))
                )):
                    measures.setdefault(row['MedicalRecord'], []).append(Measure(
                        value=row['Result'],
                        minimum=row['MinValue'],
                        maximum=row['MaxValue'],
                        at=utils.datetime_utc_serializer(row['At']),
                        type=sheba_measurement_codes.get(row['Code'], MeasureType.other),
                        external_id=row['MeasureID'],
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/measurements',
                                json={'measurements': measures})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run measurements handler.')

    def update_imaging(self, department: Departments):
        try:
            logger.debug('Getting imaging for `{}`...', department.name)
            imaging = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_images.format(unit=department.value)):
                    imaging.setdefault(row['MedicalRecord'], []).append(Image(
                        external_id=row['OrderNumber'],
                        patient_id=row['MedicalRecord'],
                        at=row['OrderDate'].astimezone(pytz.UTC).isoformat(),
                        title=row['TestName'],
                        status=SHEBA_IMAGING_STATUS.get(row['OrderStatus']),
                        interpretation=row['Result'],
                        level=SHEBA_IMAGING_LEVEL.get(row['Panic'], NotificationLevel.normal),
                        link='https://localhost/',
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/imaging', json={'images': imaging})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run imaging handler.')

    def update_labs(self, department: Departments):
        try:
            logger.debug('Getting labs for `{}`...', department.name)
            labs = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_labs.format(unit=department.value)):
                    at = row["OrderDate"].astimezone(pytz.UTC).isoformat()
                    labs.setdefault(row['MedicalRecord'], []).append(Laboratory(
                        patient_id=row['MedicalRecord'],
                        external_id=f'{row["MedicalRecord"]}#{at}#{row["TestCode"]}',
                        at=at,
                        test_type_id=row["TestCode"],
                        test_type_name=row["TestName"],
                        category_id=int(str(row["TestCode"])[0:4]),
                        category_name=CategoriesInHebrew[int(str(row["TestCode"])[0:4])],
                        test_tube_id=9,
                        panic_min_warn_bar=None,
                        min_warn_bar=row["NormMinimum"],
                        max_warn_bar=row["NormMaximum"],
                        panic_max_warn_bar=None,
                        status=(LabStatus.ordered if row["collectiondate"] is None else
                                LabStatus.collected if row["ResultTime"] is None else
                                LabStatus.analyzed)
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/labs',
                                json={"labs": labs})
            res.raise_for_status()
        except HTTPError as e:
            logger.exception(f'Could not run labs handler. {e}')

    def update_intake(self, department: Departments):
        try:
            logger.debug('Getting free_text for `{}`...', department.name)
            infos = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_intake.format(unit=department.value)):
                    if row['TextCode'] == FreeTextCodes.DOCTOR_VISIT.value:
                        intake = infos.setdefault(row['MedicalRecord'], Intake())
                        intake.doctor_seen_time = row['DocumentingTime'].astimezone(pytz.UTC).isoformat()
                    elif row['TextCode'] == FreeTextCodes.NURSE_SUMMARY.value:
                        intake = infos.setdefault(row['MedicalRecord'], Intake())
                        intake.nurse_description = row['MedicalText']
                        intake.nurse_seen_time = row['DocumentingTime'].astimezone(pytz.UTC).isoformat()
            res = requests.post(
                f'{self.dal_url}/departments/{department.name}/intake',
                json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
            )
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run basic medical handler.')

    def update_referrals(self, department: Departments):
        try:
            logger.debug('Getting referrals for `{}`...', department.name)
            referrals = {}
            treatments = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_referrals.format(unit=department.value)):
                    if row['MedicalLicense']:
                        treatments.setdefault(row['MedicalRecord'], Treatment()).doctors.append(
                            f'{row["Title"]} {row["FirstName"]} {row["LastName"]} (מ.ר. {row["MedicalLicense"]})'
                        )
                    else:
                        referrals.setdefault(row['MedicalRecord'], []).append(Referral(
                            external_id=row['ReferralId'],
                            patient_id=row['MedicalRecord'],
                            at=row['ReferralDate'].astimezone(pytz.UTC).isoformat(),
                            to=row['LastName'],
                        ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/treatments',
                                json={record: treatments[record].dict(exclude_unset=True) for record in treatments})
            res.raise_for_status()
            res = requests.post(f'{self.dal_url}/departments/{department.name}/referrals',
                                json={'referrals': referrals})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run referrals handler.')

    def update_destination(self, department: Departments):
        treatments = {}
        try:
            logger.debug('Getting treatments for `{}`...', department.name)
            with self.session() as session:
                for row in session.execute(sql_statements.query_treatment.format(unit=department.value)):
                    treatments[row["MedicalRecord"]] = \
                        Treatment(destination=row["UnitName"] or row["Decision"]).dict(exclude_unset=True)
            res = requests.post(f'{self.dal_url}/departments/{department.name}/treatments', json=treatments)
            res.raise_for_status()
        except IndexError as e:
            logger.exception("No Data Fetched From SQL", e)
        except HTTPError:
            logger.exception('Could not update treatments')

    def update_medicines(self, department: Departments):
        medicine = {}
        try:
            pass
        except IndexError as e:
            logger.exception("No Data Fetched From SQL", e)
        except HTTPError:
            logger.exception('Could not update treatments')


sheba_measurement_codes = {
    1: MeasureType.temperature,
    3: MeasureType.pulse,
    4: MeasureType.weight,
    9: MeasureType.urine_output,
    12: MeasureType.breaths,
    13: MeasureType.saturation,
    23: MeasureType.systolic,
    24: MeasureType.diastolic,
    61: MeasureType.pain,
    542: MeasureType.enriched_saturation,
}


class Departments(Enum):
    er = '1184000'


class FreeTextCodes(Enum):
    DOCTOR_VISIT = 1
    DOCTOR_SUMMARY = 889
    NURSE_SUMMARY = 901
