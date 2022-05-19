import contextlib
import os

import logbook
import requests
from requests import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ..models.arc_patient import ARCPatient
from ..models.chameleon_councils import ChameleonCouncils
from ..models.chameleon_main import ChameleonMain, Departments
from ..models.chameleon_imaging import ChameleonImaging
from ..models.chameleon_labs import ChameleonLabs
from ..models.chameleon_measurements import Measurements

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
                for measurement in session.query(Measurements). \
                        join(ChameleonMain, Measurements.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == department.name).order_by(Measurements.at.asc()):
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

    def update_councils(self, department: Departments):
        try:
            logger.debug('Getting councils for `{}`...', department.name)
            councils = {}
            with self.session() as session:
                for council in session.query(ChameleonCouncils). \
                        join(ChameleonMain, ChameleonCouncils.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == department.name).order_by(ChameleonCouncils.order_date.desc()):
                    councils.setdefault(council.patient_id, []).append(council.to_dal().dict())
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/councils',
                                json={'councils': councils})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run councils handler.')
