import contextlib
import os
from enum import Enum

import logbook
import requests
from requests import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tmr_common.data_models.measures import Temperature, Pulse, Systolic, Diastolic, Measures, BloodPressure, Saturation
from ..models.chameleon_main import ChameleonMain, Departments
from ..models.measurements import Measurements, MeasurementsIds

logger = logbook.Logger(__name__)




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
                        join(ChameleonMain, Measurements.chameleon_id == ChameleonMain.chameleon_id). \
                        where(ChameleonMain.unit == int(department.value)).order_by(Measurements.at.desc()):
                    match measurement.code:
                        case MeasurementsIds.systolic.value:
                            patients.setdefault(measurement.chameleon_id, {}).setdefault('blood_pressure', {}). \
                                setdefault('systolic', Systolic(**measurement.to_dal().dict()))
                        case MeasurementsIds.diastolic.value:
                            patients.setdefault(measurement.chameleon_id, {}).setdefault('blood_pressure', {}). \
                                setdefault('diastolic', Diastolic(**measurement.to_dal().dict()))
                        case MeasurementsIds.temperature.value:
                            patients.setdefault(measurement.chameleon_id, {}). \
                                setdefault('temperature', Temperature(**measurement.to_dal().dict()))
                        case MeasurementsIds.pulse.value:
                            patients.setdefault(measurement.chameleon_id, {}). \
                                setdefault('pulse', Pulse(**measurement.to_dal().dict()))
                        case MeasurementsIds.saturation.value:
                            patients.setdefault(measurement.chameleon_id, {}). \
                                setdefault('saturation', Saturation(**measurement.to_dal().dict()))
            measures = {
                patient: Measures(blood_pressure=BloodPressure(**patients[patient].pop('blood_pressure')),
                                  **patients[patient]).dict()
                for patient in patients
            }
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/measurements',
                                json={'measurements': measures})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run measurements handler.')
