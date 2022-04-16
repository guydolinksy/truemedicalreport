from enum import Enum

import requests
from sqlalchemy import select

from tmr_common.data_models.esi_score import ESIScore
from tmr_common.data_models.measures.blood_pressure.diastolic import Diastolic

from tmr_common.data_models.measures.blood_pressure.systolic import Systolic

from tmr_common.data_models.measures.blood_pressure.blood_pressure import BloodPressure
from tmr_common.data_models.measures.pulse import Pulse
from tmr_common.data_models.measures.temperature import Temperature

from ...models.chameleon_main import ChameleonMain
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
        patients_data_list = []
        for chameleon_patient_obj in self._get_chameleon_patient():
            single_patient_info = self._get_single_patient_info(chameleon_patient_obj)
            patients_data_list.append(single_patient_info)
        return patients_data_list

    def _get_chameleon_patient(self):
        return self._data_query.select(select(ChameleonMain))

    def _get_single_patient_info(self, patient_obj: ChameleonMain) -> Patient:
        patient_data = Patient(
            chameleon_id=patient_obj.Id_Num,
            name=patient_obj.patient_name,
            Complaint=patient_obj.Main_cause,
            awaiting="We will add this to chameleon main",
            measures=self.get_patient_measurements(patient_obj.Id_Num),
            wing=patient_obj.Unit_wing,
            bed=patient_obj.bed_num,
            unit=patient_obj.Unit,
            warnings=patient_obj.warnings)
        return patient_data

    def _get_all_patient_measurements(self, patient_id: str) -> {}:
        patient_measurements = self._data_query.select(
            select(Measurements).where(Measurements.Id_Num == patient_id))

        systolic, diastolic, temperature, pulse, blood_pressure, esi_score = None, None, None, None, None, None
        for measurement_data in patient_measurements:
            measurements_values = self._get_measurements_data(measurement_data)
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
        patients_measurements = self._get_all_patient_measurements(patients_id)[0]
        return patients_measurements

    def get_patients_esi(self, patients_id):
        patients_esi = self._get_all_patient_measurements(patients_id)[1]
        return patients_esi

    def _get_measurements_data(self, patient_measurements: Measurements):
        measurements_values = {
            "value": patient_measurements.Result,
            # "Warnings": patient_measurements.Warnings,
            "time": patient_measurements.Parameter_Date,
            "is_live": True,
            "min": patient_measurements.Min,
            "max": patient_measurements.Max
        }
        return measurements_values
