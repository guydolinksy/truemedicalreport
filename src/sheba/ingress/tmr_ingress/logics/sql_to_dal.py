import contextlib
import os
from enum import Enum

import logbook
import requests
from requests import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tmr_common.data_models.measures import Temperature, Pulse, Systolic, Diastolic
from tmr_ingress.models.chameleon_main import ChameleonMain, Departments
from tmr_ingress.models.measurements import Measurements

logger = logbook.Logger(__name__)


class MeasurementsIds(Enum):
    BloodPressure = 10
    Systolic = 101
    Diastolic = 102
    Temperature = 11
    Pulse = 12
    ESIScore = 13


class SqlToDal(object):
    def __init__(self, connection_string=None):
        connection_string = connection_string or os.getenv('CHAMELEON_CONNECTION_STRING')
        self._engine = create_engine(connection_string)

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    def update_admissions(self, department: Departments):
        try:
            logger.debug('Getting admissions for `{}`...', department.name)

            patients = []
            with self.session() as session:
                for patient in session.query(ChameleonMain).filter(ChameleonMain.unit == int(department.value)):
                    patients.append(patient.to_dal().dict())

            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/admissions',
                                json={'admissions': patients})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run admissions handler.')

    def update_measurements(self, department: Departments):
        try:
            logger.debug('Getting measurements for `{}`...', department.name)

            patients = {}
            with self.session() as session:
                for measurement in session.query(Measurements). \
                        join(ChameleonMain, Measurements.id_num == ChameleonMain.patient_id). \
                        filter(ChameleonMain.unit == int(department.value)):
                    match measurement.code:
                        case MeasurementsIds.Systolic:
                            patients.setdefault(measurement.id_num, {}).setdefault('blood_pressure', {}). \
                                setdefault('systolic', Systolic(**measurement.to_dal()).dict())
                        case MeasurementsIds.Diastolic:
                            patients.setdefault(measurement.id_num, {}).setdefault('blood_pressure', {}). \
                                setdefault('diastolic', Diastolic(**measurement.to_dal()).dict())
                        case MeasurementsIds.Temperature:
                            patients.setdefault(measurement.id_num, {}). \
                                setdefault('temperature', Temperature(**measurement.to_dal()).dict())
                        case MeasurementsIds.Pulse:
                            patients.setdefault(measurement.id_num, {}). \
                                setdefault('pulse', Pulse(**measurement.to_dal()).dict())

            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/measurements',
                                json={'measurements': patients})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run measurements handler.')
