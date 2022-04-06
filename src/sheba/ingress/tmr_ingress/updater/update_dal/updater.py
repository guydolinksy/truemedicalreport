from enum import Enum

import requests
from sqlalchemy import select

from ...models.cameleon_main import ChameleonMain
from ...models.measurements import Measurements

from ..data_query_booststrap.data_query import DataQuery

# measurements = {}
patient_db_to_dal = {"id_num": "oid",
                     "name": "name",
                     "main_cause": "complaint",
                     "true": "awaiting",
                     "false": "flagged",
                     "esi": "esi_score",
                     "unit_wing": "wing",
                     "bed_num": "bed",
                     "warnings": "warnings"}


class MeasurementsIds(Enum):
    BloodPressure = 10
    Systolic = 101
    Diastolic = 102
    Temperature = 11
    Pulse = 12
    ESIScore = 13


class DalUpdater(object):
    def __init__(self, data_query: DataQuery):
        self._data_query = data_query

    def update_all_patients(self, sql_results):
        for chameleon_patinet_obj in sql_results.scalars():
            single_patient_info = self._get_single_patient_info(chameleon_patinet_obj)
            self.post_single_patient(chameleon_patinet_obj.Id_Num, single_patient_info)

    def post_single_patient(self, patient_id: str, info: dict):
        requests.post("http://localhost/medical_dal/patient/id/" + patient_id, data=info)

    def _get_single_patient_info(self, patient_obj: ChameleonMain):
        patient_info = {}
        patient_info["oid"] = patient_obj.Id_Num
        patient_info["name"] = patient_obj.name
        patient_info["Complaint"] = patient_obj.Main_cause
        patient_info["awaiting"] = "We will add this to cameleon main"
        patient_info["measures"], patient_info["esi_score"] = self._get_patient_measurments(patient_obj.Id_Num)
        patient_info["wing"] = patient_obj.unit_wing
        patient_info["bed"] = patient_obj.bed_num
        patient_info["unit"] = patient_obj.unit
        patient_info["warnings"] = patient_obj.warnings
        return patient_info

    def _get_patient_measurments(self, patient_id: str) -> {}:
        patient_measurements = self._data_query.execute_query(
            select(Measurements).where(Measurements.id_num == patient_id))
        systolic, diastolic, temperature, pulse, blood_pressure, esi_score = {}, {}, {}, {}, {}, {}
        for measurement_data in patient_measurements.scalars().all():
            measurements_values = self._get_measurments_data(measurement_data)
            parameter_num = measurement_data.Parameter_Id
            match parameter_num:
                case MeasurementsIds.Systolic.value:
                    systolic = measurements_values
                case MeasurementsIds.Diastolic.value:
                    diastolic = measurements_values
                case MeasurementsIds.Temperature.value:
                    temperature = measurements_values
                case MeasurementsIds.Pulse.value:
                    pulse = measurements_values
                case MeasurementsIds.ESIScore.value:
                    esi_score = measurements_values

        blood_pressure = {MeasurementsIds.Systolic.name: systolic, MeasurementsIds.Diastolic.name: diastolic}
        final_measures = {
            MeasurementsIds.BloodPressure.name: blood_pressure,
            MeasurementsIds.Pulse.name: pulse,
            MeasurementsIds.Temperature.name: temperature
        }
        return final_measures, esi_score

    def _get_measurments_data(self, patient_measurements: Measurements):
        measurements_values = {
            "value": patient_measurements.Result,
            # "Warnings": patient_measurements.Warnings,
            "time": patient_measurements.Parameter_Date,
            "is_live": True
        }
        if (patient_measurements.Min is not None) and (patient_measurements.Max is not None):
            measurements_values["min"] = patient_measurements.Min
            measurements_values["max"] = patient_measurements.Max
        return measurements_values
