import contextlib
import datetime
import re
from enum import Enum
from typing import Dict, List

import logbook
import requests
from oracledb.exceptions import DatabaseError
from requests import HTTPError
from sentry_sdk import capture_message
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.data_models.admission import Admission
from common.data_models.esi_score import ESIScore
from common.data_models.image import ImagingStatus, Image
from common.data_models.labs import Laboratory, LabStatus, LabCategory
from common.data_models.measures import Measure, MeasureType
from common.data_models.notification import NotificationLevel
from common.data_models.patient import Intake, ExternalPatient, Person
from common.data_models.referrals import Referral
from common.data_models.treatment import Treatment
from .ris_adapter import OracleAdapter
from .. import config
from ..models.ris_imaging import RisImaging
from ..utils import sql_statements, utils
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
    127: ImagingStatus.analyzed,  # הפנייה לאישור
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

SHEBA_IMAGING_LINK = f'{config.care_stream_url}&accession_number={{accession_number}}'
SHEBA_LABS_LINK = f'{config.chameleon_url}/Chameleon/Asp/Records/LabResults_Modal?Patient={{patient}}'


def format_medical_summary_link(
        *, unit, record_type_code, record_char, record_part, patient_id, medical_record, hospital
):
    if record_type_code != 10:
        logger.info(f"Can't format medical summary link - unexpected record type: {record_type_code}")
        return None

    return f'{config.chameleon_url}/Chameleon/Asp/RecordsMedicalRecord/MedicalRecord' \
           f'?Unit={unit}' \
           f'&Record_Type=Emergency' \
           f'&Record_Char={record_char}' \
           f'&Record_Part={record_part}' \
           f'&Patient={patient_id}' \
           f'&Record={medical_record}' \
           f'&Hospital={hospital}'


class Departments(Enum):
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
        try:
            logger.debug('Getting admissions for `{}`...', department.name)

            patients = []
            with self.session() as session:
                for row in session.execute(sql_statements.query_patient_admission.format(unit=department.value)):
                    patients.append(ExternalPatient(
                        external_id=row["MedicalRecord"],
                        info=Person(
                            id_=row["NationalID"],
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
                        lab_link=SHEBA_LABS_LINK.format(patient=row["PatientID"]),
                        medical_summary_link=format_medical_summary_link(
                            unit=row["Unit"],
                            record_type_code=row["Record_Type"],
                            record_char=row["Record_Char"],
                            record_part=row["Answer_Code"],
                            hospital=row["Hospital"],
                            medical_record=row["MedicalRecord"]
                        )
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/admissions',
                                json={'admissions': patients})
            res.raise_for_status()

            return {'admissions': patients}
        except HTTPError:
            logger.exception('Could not run admissions handler.')

    def update_measurements(self, department: Departments):
        try:
            logger.debug('Getting measurements for `{}`...', department.name)

            measures = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_measurements.format(
                        unit=department.value, codes='({})'.format(','.join(map(str, SHEBA_MEASUREMENT_CODES)))
                )):
                    measures.setdefault(row['MedicalRecord'], []).append(Measure(
                        value=row['Result'],
                        minimum=row['MinValue'],
                        maximum=row['MaxValue'],
                        at=utils.datetime_utc_serializer(row['At']),
                        type=SHEBA_MEASUREMENT_CODES.get(row['Code'], MeasureType.other),
                        external_id=row['MeasureID'],
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/measurements',
                                json={'measurements': measures})
            res.raise_for_status()
            return {'measurements': measures}
        except HTTPError:
            logger.exception('Could not run measurements handler.')

    def update_imaging(self, department: Departments):
        try:
            imaging = []
            accessions = []
            logger.debug('Getting imaging for `{}`...', department.name)

            patients_imagings = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_images.format(unit=department.value)):
                    accessions.append(row['AccessionNumber'])
                    imaging.append(Image(
                        order_number=row['OrderNumber'],
                        external_id=row['AccessionNumber'],
                        patient_id=row['MedicalRecord'],
                        ordered_at=utils.datetime_utc_serializer(row['OrderDate']),
                        updated_at=utils.datetime_utc_serializer(
                            row['Entry_Date']) if row['Entry_Date'] else utils.datetime_utc_serializer(
                            row['OrderDate']),
                        title=row['TestName'],
                        status=SHEBA_IMAGING_STATUS.get(row['OrderStatus'], ImagingStatus.unknown),
                        interpretation=row['Result'],
                        level=SHEBA_IMAGING_LEVEL.get(row['Panic'], NotificationLevel.normal),
                        link=SHEBA_IMAGING_LINK.format(accession_number=row['AccessionNumber']),
                    ))
            self._merge_ris_chameleon_imaging(accessions, imaging)

            for image in imaging:
                logger.debug(
                    f"Load Imaging for {image.patient_id} - Accession '{image.external_id}' - '{image.dict()}'")
                patients_imagings.setdefault(image.patient_id, []).append(image.dict(exclude_unset=True))

            res = requests.post(f'{self.dal_url}/departments/{department.name}/imaging',
                                json={'images': patients_imagings})
            res.raise_for_status()
            return {'images': patients_imagings}
        except HTTPError:
            logger.exception('Could not run imaging handler.')

    def _merge_ris_chameleon_imaging(self, accessions, chameleon_imaging: List[Image]) -> None:
        try:
            ris_imagings: Dict[str, RisImaging] = self._imaging_client.query_imaging(accessions)
            logger.debug(ris_imagings)
            for imaging in chameleon_imaging:
                if ris_image := ris_imagings.get(imaging.external_id, False):
                    imaging.imaging_type = ris_image.imaging_type
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
                        lc.results.setdefault(lab["TestCode"], Laboratory(
                            patient_id=mr,
                            external_id=f'{mr}#{lc.ordered_at}#{lab["TestCode"]}',
                            ordered_at=lc.ordered_at,
                            chameleon_id=lab["TestCode"],
                            result_at=None,
                            test_type_id=lab['TestCode'],
                            test_type_name=lab['TestName'],
                            category=lab['OrderNumber'],
                            category_display_name=lab['Category'],
                            result=None,
                            units=None,
                            range=None,
                            panic=None,
                            status=LabStatus.in_progress,
                        ))
        except DatabaseError:
            capture_message('Could not query AUTODB.', level="warning")
            logger.exception('Could not query AUTODB.')

    def update_labs(self, department: Departments):
        try:
            lab_category_names = await post_dal_json("/config/get", dict(key='lab_categories', default={}))
            logger.debug('Getting labs for `{}`...', department.name)
            orders = {}
            statuses = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_lab_orders.format(unit=department.value)):
                    try:
                        status = {
                            1: LabStatus.in_progress.value,
                            2: LabStatus.analyzed.value,
                            5: LabStatus.ordered.value,
                            6: LabStatus.collected.value,
                        }[row['OrderStatus']]
                        statuses[re.sub(r'[^[0-9]', '', row['OrderNumber'])] = status

                        if status == LabStatus.analyzed.value:
                            continue
                        ordered_at = utils.datetime_utc_serializer(row["OrderDate"])
                        lc = LabCategory(
                            ordered_at=ordered_at,
                            category=row['OrderNumber'],
                            category_display_name=f"הזמנה {row['OrderNumber']}",
                            patient_id=row['MedicalRecord'],
                            status=status,
                            results={}
                        )
                        orders.setdefault(row['MedicalRecord'], {}).setdefault(lc.key, lc)
                    except KeyError as e:
                        msg = f"Lab from category '{row['OrderNumber']}' isn't exists in internal mapping " \
                              f"for medical record {row['MedicalRecord']}"
                        capture_message(msg, level="warning")
                        logger.error(msg)
            self._merge_autodb_chameleon_labs(orders)
            with self.session() as session:
                for row in session.execute(sql_statements.query_lab_results.format(unit=department.value)):
                    ordered_at = utils.datetime_utc_serializer(row["OrderDate"])
                    lc = LabCategory(
                        ordered_at=ordered_at,
                        category=row['Category'],
                        category_display_name=lab_category_names.get(row['Category'], row['Category']),
                        patient_id=row['MedicalRecord'],
                        status=statuses.get(row['OrderNumber'], LabStatus.analyzed.value),
                        results={}
                    )
                    orders.setdefault(row['MedicalRecord'], {}).setdefault(
                        lc.key, lc
                    ).results[row["TestCode"]] = self.row_to_lab(row, lab_category_names)
            labs = {mr: {c: cat.dict(exclude_unset=True) for c, cat in cats.items()} for mr, cats in orders.items()}
            res = requests.post(f'{self.dal_url}/departments/{department.name}/labs', json={"labs": labs})
            res.raise_for_status()
            return {"labs": labs}
        except HTTPError as e:
            logger.exception(f'Could not run labs handler. {e}')

    @staticmethod
    def row_to_lab(row, lab_category_names: Dict[str, str]) -> Laboratory:
        if row["ResultTime"] is None:
            status = LabStatus.ordered
            result_at = None
            logger.info(
                f"current: {datetime.datetime.utcnow()} - order: {utils.datetime_utc_serializer(row['OrderDate'])} - status: {status} - lab:{row['Row_ID']}")

        else:
            status = LabStatus.analyzed
            result_at = utils.datetime_utc_serializer(row["ResultTime"])
            logger.info(
                f"current: {datetime.datetime.utcnow()} - result: {result_at} - status: {status} -  lab:{row['Row_ID']}")

        ordered_at = utils.datetime_utc_serializer(row["OrderDate"])
        category = row["Category"].strip()
        return Laboratory(
            patient_id=row['MedicalRecord'],
            external_id=f'{row["MedicalRecord"]}#{ordered_at}#{row["TestCode"]}',
            ordered_at=ordered_at,
            chameleon_id=row["Row_ID"],
            result_at=result_at,
            test_type_id=row["TestCode"],
            test_type_name=row["TestName"],
            category=category,
            category_display_name=lab_category_names.get(category, category),
            result=row["Result"],
            units=row["Units"],
            range=row["Range"],
            panic=row["Panic"],
            status=status,
        )

    def update_doctor_intake(self, department: Departments):
        try:
            logger.debug('Getting doctor intake for `{}`...', department.name)
            infos = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_doctor_intake.format(unit=department.value)):
                    intake = infos.setdefault(row['MedicalRecord'], Intake())
                    intake.doctor_seen_time = utils.datetime_utc_serializer(row['DocumentingTime']) \
                        if row['DocumentingTime'] else None
            res = requests.post(
                f'{self.dal_url}/departments/{department.name}/intake',
                json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
            )
            res.raise_for_status()
            return {'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        except HTTPError:
            logger.exception('Could not run doctor intake handler.')

    def update_nurse_intake(self, department: Departments):
        try:
            logger.debug('Getting nurse intake for `{}`...', department.name)
            infos = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_nurse_intake.format(unit=department.value)):
                    intake = infos.setdefault(row['MedicalRecord'], Intake())
                    intake.nurse_description = row['MedicalText']
                    intake.nurse_seen_time = utils.datetime_utc_serializer(row['DocumentingTime']) \
                        if row['DocumentingTime'] else None
            res = requests.post(
                f'{self.dal_url}/departments/{department.name}/intake',
                json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
            )
            res.raise_for_status()
            return {'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        except HTTPError:
            logger.exception('Could not run nurse intake handler.')

    def update_referrals(self, department: Departments):
        try:
            logger.debug('Getting referrals for `{}`...', department.name)
            referrals = {}
            treatments = {}
            at = datetime.datetime.utcnow().isoformat()
            with self.session() as session:
                for row in session.execute(sql_statements.query_referrals.format(unit=department.value)):
                    if row['MedicalLicense']:
                        treatments.setdefault(row['MedicalRecord'], Treatment(doctors=[])).doctors.append(
                            f'{row["Title"]} {row["FirstName"]} {row["LastName"]}'
                            # TODO: (מ.ר. {row["MedicalLicense"]})'
                        )
                    else:
                        referrals.setdefault(row['MedicalRecord'], []).append(Referral(
                            external_id=row['ReferralId'],
                            patient_id=row['MedicalRecord'],
                            at=utils.datetime_utc_serializer(row['ReferralDate']) if row['ReferralDate'] else None,
                            to=row['LastName'],
                        ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/treatments',
                                json={record: treatments[record].dict(exclude_unset=True) for record in treatments})
            res.raise_for_status()
            res = requests.post(f'{self.dal_url}/departments/{department.name}/referrals',
                                json={'referrals': referrals, 'at': at})
            res.raise_for_status()
            return {'treatments': {record: treatments[record].dict(exclude_unset=True) for record in treatments},
                    'referrals': referrals, 'at': at}
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
            return {'treatments': treatments}
        except IndexError as e:
            logger.exception("No Data Fetched From SQL", e)
        except HTTPError:
            logger.exception('Could not update treatments')

    def update_medicines(self, department: Departments):
        medicine = {}
        try:
            return {'medicines': medicine}
        except IndexError as e:
            logger.exception("No Data Fetched From SQL", e)
        except HTTPError:
            logger.exception('Could not update treatments')
