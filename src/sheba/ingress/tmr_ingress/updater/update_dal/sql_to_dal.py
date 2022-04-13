from enum import Enum

import requests
from sqlalchemy import select

from tmr_common.data_models.esi_score import ESIScore
from tmr_common.data_models.measures.blood_pressure.diastolic import Diastolic

from tmr_common.data_models.measures.blood_pressure.systolic import Systolic

from tmr_common.data_models.measures.blood_pressure.blood_pressure import BloodPressure
from tmr_common.data_models.measures.pulse import Pulse
from tmr_common.data_models.measures.temperature import Temperature

from ...models.cameleon_main import CameleonMain
from ...models.measurements import Measurements
from tmr_common.data_models.measures.measures import Measures
from tmr_common.data_models.patient import Patient
from ..data_query_booststrap.data_query import DataQuery


class MeasurementsIds(Enum):
    BloodPressure = 10
    Systolic = 101
    Diastolic = 102
    Temperature = 11
    Pulse = 12
    ESIScore = 13


class SqlToDal(object):
    def __init__(self, data_query: DataQuery):
        self._data_query = data_query

    def get_all_patients(self):
        sql_results = self._get_cameleon_patient()
        patients_data_list = []
        for chameleon_patient_obj in sql_results.scalars():
            single_patient_info = self._get_single_patient_info(chameleon_patient_obj)
            patients_data_list.append(single_patient_info)
        return patients_data_list

    def _get_cameleon_patient(self):
        patients_data = self._data_query.execute_query(select(CameleonMain))
        return patients_data


    def _get_single_patient_info(self, patient_obj: CameleonMain) -> Patient:
        patient_data = Patient(
            cameleon_id=patient_obj.Id_Num,
            name=patient_obj.name,
            Complaint=patient_obj.Main_cause,
            awaiting="We will add this to cameleon main",
            measures=self.get_patient_measurements(patient_obj.Id_Num),
            wing=patient_obj.unit_wing,
            bed=patient_obj.bed_num,
            unit=patient_obj.unit,
            warnings=patient_obj.warnings)
        return patient_data

    def _get_all_patient_measurments(self, patient_id: str) -> {}:
        patient_measurements = self._data_query.execute_query(
            select(Measurements).where(Measurements.id_num == patient_id))

        systolic, diastolic, temperature, pulse, blood_pressure, esi_score = None, None, None, None, None, None
        for measurement_data in patient_measurements.scalars().all():
            measurements_values = self._get_measurments_data(measurement_data)
            parameter_num = measurement_data.Parameter_Id
            match parameter_num:
                case MeasurementsIds.Systolic.value:
                    systolic = Systolic(**measurements_values)
                case MeasurementsIds.Diastolic.value:
                    diastolic = Diastolic(**measurements_values)
                case MeasurementsIds.Temperature.value:
                    temperature = Temperature(**measurements_values)
                case MeasurementsIds.Pulse.value:
                    pulse = Pulse(**measurements_values)
                case MeasurementsIds.ESIScore.value:
                    esi_score = ESIScore(**measurements_values)

        blood_pressure = BloodPressure(systolic=systolic, diastolic=diastolic)
        patient_measures = Measures(blood_pressure=blood_pressure, pulse=pulse, temperature=temperature)
        return patient_measures, esi_score

    def get_patient_measurements(self, patients_id):
        patients_measurements = self._get_all_patient_measurments(patients_id)[0]
        return patients_measurements

    def get_patients_esi(self, patients_id):
        patients_esi = self._get_all_patient_measurments(patients_id)[1]
        return patients_esi

    def _get_measurments_data(self, patient_measurements: Measurements):
        measurements_values = {
            "value": patient_measurements.Result,
            # "Warnings": patient_measurements.Warnings,
            "time": patient_measurements.Parameter_Date,
            "is_live": True,
            "min": patient_measurements.Min,
            "max": patient_measurements.Max
        }
        return measurements_values
