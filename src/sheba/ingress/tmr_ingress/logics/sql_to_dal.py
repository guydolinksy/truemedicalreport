import contextlib
import json
import os
import random
from enum import Enum

import logbook
import requests
from requests import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tmr_common.data_models.measures import Temperature, Pulse, Systolic, Diastolic, Measures, BloodPressure, Saturation
from ..models.chameleon_main import ChameleonMain, Departments
from ..models.chameleonimaging import ChameleonImaging
from ..models.labs import ChameleonLabs
from ..models.measurements import Measurements, MeasurementsIds
from tmr_common.data_models.labs import SingleLabTest

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
                        where(ChameleonMain.unit == int(department.value)).order_by(ChameleonImaging.at.desc()):
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
                        join(ChameleonMain, Measurements.chameleon_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == int(department.value)).order_by(Measurements.at.asc()):
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

    #TODO: must be tested
    def update_labs(self, department: Departments):
        try:
            logger.debug('Getting labs for `{}`...', department.name)
            labs = {}
            with self.session() as session:
                for lab_data in session.query(ChameleonLabs). \
                        join(ChameleonMain, ChameleonLabs.patient_id == ChameleonMain.patient_id). \
                        where(ChameleonMain.unit == int(department.value)).order_by(ChameleonLabs.patient_id):
                    single_lab_test = SingleLabTest(
                        test_type_id=lab_data.test_type_id,
                        test_type_name=lab_data.test_type_name,
                        result=lab_data.result)
                    labs.setdefault(lab_data.patient_id, {})
                    if labs.category_id not in labs[lab_data.patient_id].keys():
                        labs[lab_data.patient_id][
                            labs.category_id] = labs.to_dal().dict()
                    labs[lab_data.patient_id][labs.category_id][labs.full_result].append(single_lab_test)

            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/labs',
                                json={'labs': labs})
            res.raise_for_status()
        except Exception:
            pass
