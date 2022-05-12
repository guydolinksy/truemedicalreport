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

from tmr_common.data_models.measures import Temperature, Pulse, Systolic, Diastolic, Measures, Saturation
from ..models.chameleon_main import ChameleonMain, Departments
from ..models.chameleonimaging import ChameleonImaging
from ..models.labs import ChameleonLabs
from ..models.measurements import Measurements, MeasurementsIds
from tmr_common.data_models.labs import LabTest, LabsResultsInCategory, LabsResultsOfPatient

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
                        join(ChameleonMain, ChameleonImaging.patient_id == ChameleonMain.chameleon_id). \
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

            measures = {}
            with self.session() as session:
                for measurement in session.query(Measurements). \
                        join(ChameleonMain, Measurements.patient_id == ChameleonMain.chameleon_id). \
                        where(ChameleonMain.unit == int(department.value)).order_by(Measurements.at.asc()):
                    measures.setdefault(measurement.patient_id, []).append(measurement.to_dal().dict())

            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/measurements',
                                json={'measurements': measures})
            res.raise_for_status()
        except HTTPError:
            logger.exception('Could not run measurements handler.')

    # TODO: request fails on 422, needs a fix
    def update_labs(self, department: Departments):
        try:
            logger.debug('Getting labs for `{}`...', department.name)
            labs = {}
            with self.session() as session:
                labs_table_data = session.query(ChameleonLabs). \
                    join(ChameleonMain, ChameleonLabs.patient_id == ChameleonMain.chameleon_id). \
                    where(ChameleonMain.unit == int(department.value)).order_by(ChameleonLabs.patient_id)
                for lab_data in labs_table_data:
                    single_lab_test = lab_data.to_initial_dal()
                    labs.setdefault(lab_data.patient_id, {})
                    if lab_data.category_id not in labs[lab_data.patient_id].keys():
                        labs[lab_data.patient_id][
                            lab_data.category_id] = []
                    labs[lab_data.patient_id][lab_data.category_id].append(single_lab_test)
            final_result = {}
            for patient_id in labs:
                final_result[patient_id] = []
                labs_results_of_patient = LabsResultsOfPatient(patient_id=patient_id, lab_results=[])
                for category_id in labs[patient_id].keys():
                    labs_results_in_cat = LabsResultsInCategory(category_id=category_id, category_results=[])
                    for lab_result in labs[patient_id][category_id]:
                        labs_results_in_cat.category_results.append(lab_result.dict())
                    labs_results_of_patient.lab_results.append(labs_results_in_cat.dict())
                    final_result[patient_id].append(labs_results_of_patient.dict())
            res = requests.post(f'http://medical-dal/medical-dal/departments/{department.name}/labs',
                                json={"labs": final_result})
            print(res.content)
            res.raise_for_status()
        except HTTPError as e:
            logger.exception(f'Could not run labs handler. {e}')
