import os
from typing import List, Tuple, Optional
import logbook
import pytz

from fastapi import APIRouter

from common.data_models.mci import MCIResult
from digest import config
from digest.utils.utils import fetch_dal_json, post_dal_json
from common.graphql.graphql import GraphQLQuery, GraphQLModel
import datetime

mci_router = APIRouter()
logger = logbook.Logger(__name__)


@mci_router.get('/form')
async def get_form_options():
    return await fetch_dal_json("/mci/form")


class GetDataQueryResponsePatientInfo(GraphQLModel):
    id_: str
    name: str


class GetDataQueryResponsePatientAdmission(GraphQLModel):
    arrival: str
    wing_id: str


class GetDataQueryResponsePatientMCIStringValue(GraphQLModel):
    value: str
    at: str


class GetDataQueryResponsePatientMCIListItem(GraphQLModel):
    key: str
    value: str
    at: str


class GetDataQueryResponsePatientMCI(GraphQLModel):
    occupation: GetDataQueryResponsePatientMCIStringValue
    transport: GetDataQueryResponsePatientMCIStringValue
    diagnosis: List[GetDataQueryResponsePatientMCIListItem]
    pre_hospital_treatment: List[GetDataQueryResponsePatientMCIListItem]
    hospital_treatment: List[GetDataQueryResponsePatientMCIListItem]
    imaging: List[GetDataQueryResponsePatientMCIListItem]


class GetDataQueryResponsePatientMCIResult(GraphQLModel):
    real_date: str
    execution_date: str
    parameter: str
    result: str


class GetDataQueryResponsePatient(GraphQLModel):
    admission: GetDataQueryResponsePatientAdmission
    info: GetDataQueryResponsePatientInfo
    external_id: str

    mci: GetDataQueryResponsePatientMCI
    mci_results: List[GetDataQueryResponsePatientMCIResult]

    def __init__(self, *args, **kwargs):  # TODO
        if not kwargs.get('mci_results'):
            kwargs['mci_results'] = []
        super().__init__(*args, **kwargs)


class GetDataQueryResponsePatients(GraphQLModel):
    patients: List[GetDataQueryResponsePatient]


class GetData(GraphQLQuery):
    getPatients: GetDataQueryResponsePatients


# TODO: ADD it as config
parameter_codes = {
    'occupation': '5219',
    'transport': '5219',
    'diagnosis': '5220',
    'pre_hospital_treatment': '5221',
    'hospital_treatment': '5222',
    'imaging': '5223',
}


def to_mssql_date(d):
    return datetime.datetime.fromisoformat(d.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M:%S")

def round_seconds(d):
    return  datetime.datetime.fromisoformat(d.replace('Z', '+00:00')).replace(second=0, microsecond=0).isoformat()

def get_results(patient) -> List[MCIResult]:
    results_list = []

    occupation = MCIResult(
        real_date=patient.mci.occupation.at,
        execution_date=round_seconds(patient.mci.occupation.at),
        parameter=parameter_codes['occupation'],
        result=patient.mci.occupation.value
    )
    results_list.append(occupation)
    transport = MCIResult(
        real_date=patient.mci.transport.at,
        execution_date=round_seconds(patient.mci.transport.at),
        parameter=parameter_codes['transport'],
        result=patient.mci.transport.value
    )
    results_list.append(transport)

    for diagnosis in patient.mci.diagnosis:
        diagnoses = MCIResult(
            real_date=diagnosis.at,
            execution_date=round_seconds(diagnosis.at),
            parameter=parameter_codes['diagnosis'],
            result=diagnosis.value
        )
        results_list.append(diagnoses)

    for pre_hospital_treatment in patient.mci.pre_hospital_treatment:
        pre_hospital_treatments = MCIResult(
            real_date=pre_hospital_treatment.at,
            execution_date=round_seconds(pre_hospital_treatment.at),
            parameter=parameter_codes['pre_hospital_treatment'],
            result=pre_hospital_treatment.value
        )
        results_list.append(pre_hospital_treatments)

    for hospital_treatment in patient.mci.hospital_treatment:
        hospital_treatments = MCIResult(
            real_date=hospital_treatment.at,
            execution_date=round_seconds(hospital_treatment.at),
            parameter=parameter_codes['hospital_treatment'],
            result=hospital_treatment.value
        )
        results_list.append(hospital_treatments)

    for imaging in patient.mci.imaging:
        imagings = MCIResult(
            real_date=imaging.at,
            execution_date=round_seconds(imaging.at),
            parameter=parameter_codes['imaging'],
            result=imaging.value
        )
        results_list.append(imagings)

    return results_list


def correct(result: MCIResult, stored_results: List[MCIResult]) -> MCIResult:
    taken = {res.execution_date for res in stored_results if res.parameter == result.parameter}

    execution_date = result.execution_date
    while execution_date in taken:
        execution_date = (datetime.datetime.fromisoformat(execution_date) + datetime.timedelta(minutes=1)).isoformat()

    return MCIResult(
        real_date=result.real_date,
        execution_date=execution_date,
        parameter=result.parameter,
        result=result.result,
    )


def process_results(
        results: List[MCIResult],
        previous_results: List[GetDataQueryResponsePatientMCIResult],
        safety_buffer: int
) -> Tuple[List[MCIResult], List[MCIResult]]:
    results_for_chameleon = []
    stored_results = [MCIResult(**previous_result.model_dump()) for previous_result in previous_results]
    threshold = (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=safety_buffer)).isoformat()
    for result in results:
        if result.real_date > threshold:
            continue
        if any(previous_result for previous_result in previous_results if
               (result.real_date, result.parameter, result.result) ==
               (previous_result.real_date, previous_result.parameter, previous_result.result)):
            continue

        corrected_result = correct(result.copy(), stored_results)

        stored_results.append(corrected_result)
        results_for_chameleon.append(corrected_result)
    assert not any(problems := [[
        (result_for_chameleon, previous_result) for result_for_chameleon in results_for_chameleon if
        previous_result.execution_date == result_for_chameleon.execution_date and
        previous_result.parameter == result_for_chameleon.parameter
    ] for previous_result in previous_results]), problems
    return stored_results, results_for_chameleon


async def mci_data(safety_buffer: int):
    all_results_for_chameleon = []
    for patient in (await GetData.run_query(config.graphql_url, {
        'getPatients(department: "mci")': GetDataQueryResponsePatients,
    })).getPatients.patients:
        results = get_results(patient)
        stored_results, results_for_chameleon = process_results(results, patient.mci_results, safety_buffer)
        data = {
            "User": "",  # os.getenv("DB_User"),
            "Password": "",  # os.getenv("DB_Pass"),
            "IdNum": patient.info.id_,
            "Patient": "",
            "MedicalRecord": patient.external_id.replace('mci#', ''),
            "Results": [{
                'ExecutionDate': to_mssql_date(r.execution_date),
                'Parameter': r.parameter,
                'Result': r.result,
            } for r in results_for_chameleon]
        }

        await post_dal_json("/mci/mci_to_mongo",
                            json_payload={
                                'results': [a.model_dump() for a in stored_results],
                                'id_': patient.info.id_
                            })
        all_results_for_chameleon += results_for_chameleon

    return all_results_for_chameleon
