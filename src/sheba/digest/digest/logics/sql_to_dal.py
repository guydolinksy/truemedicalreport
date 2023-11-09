import asyncio
import contextlib
import datetime
import re
from enum import Enum
from typing import Dict

import logbook
import pytz
import requests
from oracledb.exceptions import DatabaseError
from requests import HTTPError
from sentry_sdk import capture_message
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from common.data_models.admission import Admission
from common.data_models.discussion import Note
from common.data_models.esi_score import ESIScore
from common.data_models.image import ImagingStatus, Image
from common.data_models.labs import Laboratory, LabStatus, LabCategory
from common.data_models.measures import Measure, MeasureType
from common.data_models.notification import NotificationLevel
from common.data_models.patient import Intake, ExternalData
from common.data_models.person import Person
from common.data_models.referrals import Referral
from .ris_adapter import OracleAdapter
from .. import config
from ..models.ris_imaging import RisImaging
from ..utils import sql_statements, utils
from ..utils.sql_statements import PatientAdmissionQuery, MeasurementsQuery, ImagesQuery, ReferralsQuery, \
    DestinationsQuery, LabOrdersQuery, LabResultsQuery, DoctorNotesQuery, DoctorIntakeQuery, NurseIntakeQuery, \
    LabInProgressQuery
from ..utils.utils import post_dal_json

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
    127: ImagingStatus.ordered,  # הפנייה לאישור
}
SHEBA_IMAGING_LEVEL = {
    0: NotificationLevel.normal,
    1: NotificationLevel.panic,
}

SHEBA_MEASUREMENT_CODES = {
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
SHEBA_MEASUREMENT_MINIMUMS = {
    MeasureType.systolic: '90',
    MeasureType.pulse: '50',
    MeasureType.temperature: '35',
    MeasureType.saturation: '93',
    MeasureType.pain: '0',
}
SHEBA_MEASUREMENT_MAXIMUMS = {
    MeasureType.systolic: '180',
    MeasureType.pulse: '120',
    MeasureType.temperature: '38',
    MeasureType.saturation: '100',
    MeasureType.pain: '5',
}

SHEBA_IMAGING_LINK = f'{config.care_stream_url}&accession_number={{accession_number}}'
SHEBA_LABS_LINK = f'{config.chameleon_url}/Chameleon/Asp/Records/LabResults_Modal?Patient={{patient}}'

SHEBA_MCI_REFERRAL_CODE = 'פא'


def format_medical_summary_link(
        *, unit, record_type_code, record_char, record_part, patient_id, medical_record, hospital
):
    if record_type_code != 10:
        logger.info(f"Can't format medical summary link - unexpected record type: {record_type_code}")
        return None

    return (f'{config.chameleon_url}/Chameleon/Asp/RecordsMedicalRecord/MedicalRecord?Unit={unit}&Record_Type=Emergency'
            f'&Record_Char={record_char}&Record_Part={record_part}&Patient={patient_id}&Record={medical_record}'
            f'&Hospital={hospital}')


class Departments(str, Enum):
    er = '1184000'


class SqlToDal(object):
    def __init__(self, chameleon_connection=None, dal_url=None, labs_params=None, imaging_params=None):
        self.dal_url = dal_url or config.dal_url

        chameleon_connection = chameleon_connection or config.chameleon_connection
        self._engine = create_engine(chameleon_connection)

        imaging_connection_params = imaging_params or config.imaging_params
        self._imaging_client = OracleAdapter(imaging_connection_params)

        labs_connection_params = labs_params or config.labs_params
        self._labs_client = OracleAdapter(labs_connection_params)

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    def update_admissions(self, department: Departments):
        logger.debug('Getting admissions for `{}`...', department.name)

        patients = []
        at = datetime.datetime.now(tz=pytz.UTC).isoformat()
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_patient_admission.format(unit=department))):
                # print(row[PatientAdmissionQuery.ROOM_CODE])
                patients.append(ExternalData(
                    external_id=str(row[PatientAdmissionQuery.MEDICAL_RECORD]),
                    info=Person(
                        id_=row[PatientAdmissionQuery.NATIONAL_ID],
                        name=row[PatientAdmissionQuery.FULL_NAME],
                        gender='male' if row[PatientAdmissionQuery.GENDER] == 'זכר' else 'female',
                        birthdate=utils.datetime_utc_serializer(row[PatientAdmissionQuery.BIRTH_DATE]),
                        age=utils.calculate_patient_age(row[PatientAdmissionQuery.BIRTH_DATE]),
                        phone=row[PatientAdmissionQuery.PHONE]
                    ),
                    esi=ESIScore(
                        value=int(row[PatientAdmissionQuery.ESI]),
                        at=utils.datetime_utc_serializer(row[PatientAdmissionQuery.ADMISSION_DATE]),
                    ) if row[PatientAdmissionQuery.ESI] else None,
                    admission=Admission(
                        department_id=department.value,
                        wing_id=str(row[PatientAdmissionQuery.ROOM_CODE]),
                        bed=row[PatientAdmissionQuery.BED_NAME],
                        arrival=utils.datetime_utc_serializer(row[PatientAdmissionQuery.ADMISSION_DATE]),
                    ),
                    intake=Intake(
                        complaint=row[PatientAdmissionQuery.MAIN_CAUSE],
                    ),
                    lab_link=SHEBA_LABS_LINK.format(patient=row[PatientAdmissionQuery.PATIENT_ID]),
                    medical_summary_link=format_medical_summary_link(
                        unit=row[PatientAdmissionQuery.UNIT],
                        record_type_code=row[PatientAdmissionQuery.RECORD_TYPE],
                        record_char=row[PatientAdmissionQuery.RECORD_CHAR],
                        record_part=row[PatientAdmissionQuery.ANSWER_CODE],
                        patient_id=row[PatientAdmissionQuery.PATIENT_ID],
                        medical_record=row[PatientAdmissionQuery.MEDICAL_RECORD],
                        hospital=row[PatientAdmissionQuery.HOSPITAL],
                    )).model_dump(exclude_unset=True))
        res = requests.post(f'{self.dal_url}/departments/{department.value}/admissions',
                            json={'admissions': patients, 'at': at})
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'admissions': patients}
        except HTTPError:
            logger.exception('Could not run admissions handler. {}', res.json() if res else '')

    def update_measurements(self, department: Departments):
        logger.debug('Getting measurements for `{}`...', department.name)

        measures = {}
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_measurements.format(
                    unit=department, codes='({})'.format(','.join(map(str, SHEBA_MEASUREMENT_CODES)))
            ))):
                if row[MeasurementsQuery.RESULT] is not None:
                    code = SHEBA_MEASUREMENT_CODES.get(row[MeasurementsQuery.CODE], MeasureType.other)
                    measures.setdefault(row[MeasurementsQuery.MEDICAL_RECORD], []).append(Measure(
                        value=row[MeasurementsQuery.RESULT],
                        minimum=SHEBA_MEASUREMENT_MINIMUMS.get(code),  # row['MinValue'],
                        maximum=SHEBA_MEASUREMENT_MAXIMUMS.get(code),  # row['MaxValue'],
                        at=utils.datetime_utc_serializer(row[MeasurementsQuery.AT]),
                        type=code,
                        external_id=row[MeasurementsQuery.MEASURE_ID],
                    ).model_dump(exclude_unset=True))
        res = requests.post(f'{self.dal_url}/departments/{department.value}/measurements',
                            json={'measurements': measures})
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'measurements': measures}
        except HTTPError:
            logger.exception('Could not run measurements handler. {}', res.json() if res else '')

    def update_imaging(self, department: Departments):
        imaging = {}
        accessions = []
        logger.debug('Getting imaging for `{}`...', department.name)

        with self.session() as session:
            for row in session.execute(text(sql_statements.query_images.format(unit=department))):
                accessions.append(row[ImagesQuery.ACCESSION_NUMBER])
                i = Image(
                    accession_number=row[ImagesQuery.ACCESSION_NUMBER],
                    order_number=row[ImagesQuery.ORDER_NUMBER],
                    ordered_at=utils.datetime_utc_serializer(row[ImagesQuery.ORDER_DATE]),
                    updated_at=utils.datetime_utc_serializer(row[ImagesQuery.ENTRY_DATE]) if row[
                        ImagesQuery.ENTRY_DATE] else utils.datetime_utc_serializer(row[ImagesQuery.ORDER_DATE]),
                    title=row[ImagesQuery.TEST_NAME],
                    status=SHEBA_IMAGING_STATUS.get(row[ImagesQuery.ORDER_STATUS], ImagingStatus.unknown),
                    interpretation=row[ImagesQuery.RESULT] if row[ImagesQuery.RESULT] else None,
                    level=SHEBA_IMAGING_LEVEL.get(row[ImagesQuery.PANIC], NotificationLevel.normal),
                    link=SHEBA_IMAGING_LINK.format(accession_number=row[ImagesQuery.ACCESSION_NUMBER]),
                )
                imaging.setdefault(row[ImagesQuery.MEDICAL_RECORD], {}).__setitem__(i.external_id, i)
        self._merge_ris_chameleon_imaging(accessions, imaging)

        res = requests.post(f'{self.dal_url}/departments/{department.value}/imaging', json={'images': {
            p: {e: i.model_dump(exclude_unset=True) for e, i in imaging[p].items()} for p in imaging
        }})
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'images': imaging}
        except HTTPError:
            logger.exception('Could not run imaging handler. {}', res.json() if res else '')

    def _merge_ris_chameleon_imaging(self, accessions, chameleon_imaging: Dict[str, Dict[str, Image]]) -> None:
        try:
            ris_imagings: Dict[str, RisImaging] = self._imaging_client.query_imaging(accessions)

            for patient in chameleon_imaging:
                for external_id in chameleon_imaging[patient]:
                    if ris_image := ris_imagings.get(external_id, False):
                        chameleon_imaging[patient][external_id].imaging_type = ris_image.imaging_type
        except DatabaseError:
            capture_message('Could not query RIS.', level="warning")
            logger.exception('Could not query RIS.')

    def _merge_autodb_chameleon_labs(self, orders: Dict[str, Dict[str, LabCategory]]) -> None:
        try:
            order_numbers = [lc.category for mr, lcs in orders.items() for key, lc in lcs.items()]
            labs = self._labs_client.query_labs(order_numbers=order_numbers)
            for mr, lcs in orders.items():
                for key, lc in lcs.items():
                    for lab in labs.get(lc.category, []):
                        l = Laboratory(
                            ordered_at=lc.ordered_at,
                            result_at=None,
                            test_type_id=lab[LabInProgressQuery.TEST_CODE],
                            test_type_name=lab[LabInProgressQuery.TEST_NAME],
                            category=lc.category,
                            category_display_name=str(lab[LabInProgressQuery.CATEGORY]),
                            result=None,
                            units=None,
                            range=None,
                            panic=None,
                            status=LabStatus.in_progress,
                        )
                        lc.results.setdefault(l.external_id, l)
        except DatabaseError:
            capture_message('Could not query AUTODB.', level="warning")
            logger.exception('Could not query AUTODB.')

    def update_labs(self, department: Departments):
        lab_category_names = asyncio.run(post_dal_json("/config/get", dict(key='lab_categories', default={})))
        logger.debug('Getting labs for `{}`...', department.name)
        orders = {}
        statuses = {}
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_lab_orders.format(unit=department))):
                try:
                    status = {
                        1: LabStatus.in_progress,
                        2: LabStatus.analyzed,
                        5: LabStatus.ordered,
                        6: LabStatus.collected,
                    }[row[LabOrdersQuery.ORDER_STATUS]]
                    statuses[re.sub(r'[^[0-9]', '', row[LabOrdersQuery.ORDER_NUMBER])] = status

                    if status == LabStatus.analyzed:
                        continue
                    ordered_at = utils.datetime_utc_serializer(row[LabOrdersQuery.ORDER_DATE])
                    lc = LabCategory(
                        ordered_at=ordered_at,
                        category=row[LabOrdersQuery.ORDER_NUMBER],
                        category_display_name=f"הזמנה {row[LabOrdersQuery.ORDER_NUMBER]}",
                        status=status,
                        results={}
                    )
                    orders.setdefault(row[LabOrdersQuery.MEDICAL_RECORD], {}).setdefault(lc.external_id, lc)
                except KeyError as e:
                    msg = f"Lab from category '{row[LabOrdersQuery.ORDER_NUMBER]}' isn't exists in internal mapping " \
                          f"for medical record {row[LabOrdersQuery.MEDICAL_RECORD]}"
                    capture_message(msg, level="warning")
        self._merge_autodb_chameleon_labs(orders)
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_lab_results.format(unit=department))):
                l = self.row_to_lab(row, lab_category_names)
                lc = LabCategory(
                    ordered_at=utils.datetime_utc_serializer(row[LabResultsQuery.ORDER_DATE]),
                    category=row[LabResultsQuery.CATEGORY],
                    category_display_name=lab_category_names.get(row[LabResultsQuery.CATEGORY],
                                                                 str(row[LabResultsQuery.CATEGORY])),
                    status=statuses.get(row[LabResultsQuery.ORDER_NUMBER], LabStatus.analyzed),
                    results={}
                )
                orders.setdefault(row[LabResultsQuery.MEDICAL_RECORD], {}). \
                    setdefault(lc.external_id, lc).results[l.external_id] = l
        labs = {mr: {c: cat.dict(exclude_unset=True) for c, cat in cats.items()} for mr, cats in orders.items()}
        res = requests.post(f'{self.dal_url}/departments/{department.value}/labs', json={"labs": labs})
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {"labs": labs}
        except HTTPError:
            logger.exception('Could not run labs handler. {}', res.json() if res else '')

    @staticmethod
    def row_to_lab(row, lab_category_names: Dict[str, str]) -> Laboratory:
        if row[LabResultsQuery.RESULT_TIME] is None:
            status = LabStatus.ordered
            result_at = None
        else:
            status = LabStatus.analyzed
            result_at = utils.datetime_utc_serializer(row[LabResultsQuery.RESULT_TIME])

        ordered_at = utils.datetime_utc_serializer(row[LabResultsQuery.ORDER_DATE])
        category = row[LabResultsQuery.CATEGORY].strip()
        return Laboratory(
            ordered_at=ordered_at,
            result_at=result_at,
            test_type_id=row[LabResultsQuery.TEST_CODE],
            test_type_name=row[LabResultsQuery.TEST_NAME],
            category=category,
            category_display_name=lab_category_names.get(category, category),
            result=row[LabResultsQuery.RESULT],
            units=row[LabResultsQuery.UNITS],
            range=row[LabResultsQuery.RANGE],
            panic=row[LabResultsQuery.PANIC],
            status=status,
        )

    def update_doctor_notes(self, department: Departments):
        notes = {}
        logger.debug('Getting doctor notes for `{}`...', department.name)
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_doctor_notes.format(unit=department))):
                n = Note(
                    follow_up_id=str(row[DoctorNotesQuery.FOLLOW_UP_ID]),
                    subject=row[DoctorNotesQuery.SUBJECT],
                    content=row[DoctorNotesQuery.MEDICAL_TEXT],
                    by=f'{row[DoctorNotesQuery.TITLE]} {row[DoctorNotesQuery.FIRST_NAME]} {row[DoctorNotesQuery.LAST_NAME]}',
                    at=utils.datetime_utc_serializer(row[DoctorNotesQuery.NOTE_DATE]),
                )
                notes.setdefault(row[DoctorNotesQuery.MEDICAL_RECORD], {}).__setitem__(n.external_id, n)
        res = requests.post(
            f'{self.dal_url}/departments/{department.value}/discussion',
            json={'notes': {record: {id_: note.dict(exclude_unset=True) for id_, note in notes[record].items()} for
                            record in notes}}
        )
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'notes': {
                record: {id_: note.dict(exclude_unset=True) for id_, note in notes[record].items()} for record in notes
            }}
        except HTTPError:
            logger.exception('Could not run doctor notes handler. {}', res.json() if res else '')

    def update_doctor_intake(self, department: Departments):
        logger.debug('Getting doctor intake for `{}`...', department.name)
        infos = {}
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_doctor_intake.format(unit=department))):
                intake = infos.setdefault(row[DoctorIntakeQuery.MEDICAL_RECORD], Intake())
                intake.doctor_seen_time = utils.datetime_utc_serializer(row[DoctorIntakeQuery.DOCUMENTING_TIME]) \
                    if row[DoctorIntakeQuery.DOCUMENTING_TIME] else None
        res = requests.post(
            f'{self.dal_url}/departments/{department.value}/intake_doctor',
            json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        )
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        except HTTPError:
            logger.exception('Could not run doctor intake handler. {}', res.json() if res else '')

    def update_nurse_intake(self, department: Departments):
        logger.debug('Getting nurse intake for `{}`...', department.name)
        infos = {}
        mci_patients = []
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_nurse_intake.format(unit=department))):
                intake = infos.setdefault(row[NurseIntakeQuery.MEDICAL_RECORD], Intake())
                intake.nurse_description = row[NurseIntakeQuery.MEDICAL_TEXT]
                intake.nurse_seen_time = utils.datetime_utc_serializer(row[NurseIntakeQuery.DOCUMENTING_TIME]) \
                    if row[NurseIntakeQuery.DOCUMENTING_TIME] else None

                if row[NurseIntakeQuery.REFERRAL_CODE] == SHEBA_MCI_REFERRAL_CODE:
                    mci_patients.append(str(row[NurseIntakeQuery.MEDICAL_RECORD]))
        res = requests.post(
            f'{self.dal_url}/departments/{department.value}/intake_nurse',
            json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        )
        try:
            # logger.debug(res.json())
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run nurse intake handler. {}', res.json() if res else '')

        res = requests.post(
            f'{self.dal_url}/departments/mci/intake', json={'intake': mci_patients}
        )
        try:
            # logger.debug(res.json())
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run mci hanfler. {}', res.json() if res else '')

        return {
            'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos},
            'mci_intake': mci_patients
        }

    def update_referrals(self, department: Departments):
        logger.debug('Getting referrals for `{}`...', department.name)
        referrals = {}
        doctors = {}
        at = datetime.datetime.now(tz=pytz.UTC).isoformat()
        with self.session() as session:
            for row in session.execute(text(sql_statements.query_referrals.format(unit=department))):
                if row[ReferralsQuery.MEDICAL_LICENSE]:
                    doctors.setdefault(row[ReferralsQuery.MEDICAL_RECORD], []).append(
                        f'{row[ReferralsQuery.TITLE]} {row[ReferralsQuery.FIRST_NAME]} {row[ReferralsQuery.LAST_NAME]}'
                        # TODO: (מ.ר. {row["MedicalLicense"]})'
                    )
                else:
                    referrals.setdefault(row[ReferralsQuery.MEDICAL_RECORD], {}).__setitem__(
                        row[ReferralsQuery.REFERRAL_ID], Referral(
                            at=utils.datetime_utc_serializer(row[ReferralsQuery.REFERRAL_DATE]) if row[
                                ReferralsQuery.REFERRAL_DATE] else None,
                            to=row[ReferralsQuery.LAST_NAME],
                        ).model_dump(exclude_unset=True))
        res = requests.post(f'{self.dal_url}/departments/{department.value}/doctors',
                            json={'doctors': doctors})
        try:
            # logger.debug(res.json())
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run referrals handler. {}', res.json() if res else None)
            return

        res = requests.post(f'{self.dal_url}/departments/{department.value}/referrals',
                            json={'referrals': referrals, 'at': at})
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'doctors': doctors, 'referrals': referrals, 'at': at}
        except HTTPError:
            logger.exception('Could not run referrals handler. {}', res.json() if res else None)

    def update_destination(self, department: Departments):
        logger.debug('Getting destinations for `{}`...', department.name)
        destinations = {}
        with (self.session() as session):
            for row in session.execute(text(sql_statements.query_destinations.format(unit=department))):
                destinations[row[DestinationsQuery.MEDICAL_RECORD]] = \
                    row[DestinationsQuery.UNIT_NAME] or row[DestinationsQuery.DECISION]
        res = requests.post(f'{self.dal_url}/departments/{department.value}/destinations',
                            json=dict(destinations=destinations))
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'destinations': destinations}
        except HTTPError:
            logger.exception('Could not update destinations. {}', res.json() if res else None)

    def update_medications(self, department: Departments):
        medications = {}
        with (self.session() as session):
            for row in session.execute(text(sql_statements.query_medications.format(unit=department))):
                medications[row] = 0
        res = requests.post(f'{self.dal_url}/departments/{department.value}/medications', json=medications)
        try:
            # logger.debug(res.json())
            res.raise_for_status()
            return {'medications': medications}
        except HTTPError:
            logger.exception('Could not update treatments. {}', res.json() if res else None)
