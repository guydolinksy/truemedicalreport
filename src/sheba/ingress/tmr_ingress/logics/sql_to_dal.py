import contextlib
import json
import os

import logbook
import requests
from requests import HTTPError
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session

from tmr_common.data_models.patient import BasicMedical
from ..models.arc_patient import ARCPatient
from ..models.chameleon_referrals import ChameleonReferrals
from ..models.chameleon_main import ChameleonMain, Departments
from ..models.chameleon_imaging import ChameleonImaging
from ..models.chameleon_labs import ChameleonLabs
from ..models.chameleon_measurements import ChameleonMeasurements
from ..models.chameleon_medical_free_text import ChameleonMedicalText, FreeTextCodes, Units

logger = logbook.Logger(__name__)


class SqlToDal(object):
    def __init__(self, connection_string=None):
        connection_string = connection_string or os.getenv('CHAMELEON_CONNECTION_STRING')
        self._engine = create_engine(connection_string)

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    # TODO validate the data inside json parameter can be accepted succecfully on dal
    def update_imaging(self, department: Departments):
        try:
            logger.debug('Getting imaging for `{}`...', department.name)
            imaging = {}
            with self.session() as session:
                for image in session.query(ChameleonImaging). \
                        join(ChameleonMain, ChameleonImaging.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == department.name).order_by(ChameleonImaging.order_date.desc()):
                    imaging.setdefault(image.patient_id, []).append(image.to_dal().dict())
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/imaging',
                                json={'images': imaging})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run imaging handler.')

    def update_admissions(self, department: Departments):
        try:
            logger.debug('Getting admissions for `{}`...', department.name)

            patients = []
            with self.session() as session:
                for patient in session.query(ChameleonMain).filter(ChameleonMain.unit == department.name):
                    data = session.query(ARCPatient).filter(ARCPatient.patient_id == patient.patient_id).first()
                    patients.append(dict(**data.to_dal(), **patient.to_dal()))

            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/admissions',
                                json={'admissions': patients})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run admissions handler.')

    def update_measurements(self, department: Departments):
        try:
            logger.debug('Getting measurements for `{}`...', department.name)

            measures = {}
            with self.session() as session:
                for measurement in session.query(ChameleonMeasurements). \
                        join(ChameleonMain, ChameleonMeasurements.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == department.name).order_by(ChameleonMeasurements.at.asc()):
                    measures.setdefault(measurement.patient_id, []).append(measurement.to_dal().dict())

            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/measurements',
                                json={'measurements': measures})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run measurements handler.')

    def update_labs(self, department: Departments):
        try:
            logger.debug('Getting labs for `{}`...', department.name)
            labs = {}
            with self.session() as session:
                for lab_data in session.query(ChameleonLabs). \
                        join(ChameleonMain, ChameleonLabs.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == department.name).order_by(ChameleonLabs.patient_id):
                    labs.setdefault(lab_data.patient_id, []).append(lab_data.to_initial_dal().dict())
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/labs',
                                json={"labs": labs})
            res.raise_for_status()
        except HTTPError as e:
            logger.exception(f'Could not run labs handler. {e}')

    def update_basic_medical(self, department: Departments):
        try:
            logger.debug('Getting free_text for `{}`...', department.name)
            infos = {}
            with self.session() as session:
                for free_text in session.query(ChameleonMedicalText).filter(ChameleonMedicalText.medical_text_code.in_([
                    FreeTextCodes.DOCTOR_VISIT.value, FreeTextCodes.NURSE_SUMMARY.value
                ])):
                    free_text.update_basic_medical(infos.setdefault(free_text.patient_id, BasicMedical()))
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/basic_medical',
                                json={'basic_medicals': {patient: infos[patient].dict() for patient in infos}})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run basic medical handler.')

    def update_referrals(self, department: Departments):
        try:
            logger.debug('Getting referrals for `{}`...', department.name)
            referrals = {}
            with self.session() as session:
                for referral in session.query(ChameleonReferrals). \
                        join(ChameleonMain, ChameleonReferrals.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == department.name).order_by(ChameleonReferrals.order_date.desc()):
                    referrals.setdefault(referral.patient_id, []).append(referral.to_dal().dict())
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/referrals',
                                json={'referrals': referrals})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run referrals handler.')
