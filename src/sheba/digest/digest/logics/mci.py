import datetime
from typing import List, Tuple, Optional

import aiohttp
import logbook
import pytz
from aiohttp import BasicAuth

from common.data_models.mci import MCIResult
from common.graphql.graphql import GraphQLQuery, GraphQLModel
from common.mci import MCI_MANUAL_IDENTITY
from digest import config
from digest.config import ParameterCodes
from digest.utils.utils import post_dal_json

logger = logbook.Logger(__name__)


class GetDataQueryResponsePatientInfo(GraphQLModel):
    id_: str
    patient: str
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
    short_value: Optional[str] = None
    at: str
    customizer: Optional[str] = None


class GetDataQueryResponsePatientMCI(GraphQLModel):
    occupation: Optional[GetDataQueryResponsePatientMCIStringValue]
    transport: Optional[GetDataQueryResponsePatientMCIStringValue]
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
    source_identity: Optional[str]

    def __init__(self, *args, **kwargs):  # TODO
        if not kwargs.get('mci_results'):
            kwargs['mci_results'] = []
        super().__init__(*args, **kwargs)


class GetDataQueryResponsePatients(GraphQLModel):
    patients: List[GetDataQueryResponsePatient]


class GetData(GraphQLQuery):
    getPatients: GetDataQueryResponsePatients


def to_mssql_date(d):
    return datetime.datetime.fromisoformat(d.replace('Z', '+00:00')).astimezone(
        pytz.timezone('Asia/Jerusalem')
    ).strftime("%Y-%m-%d %H:%M:%S")


def round_seconds(d):
    return datetime.datetime.fromisoformat(d.replace('Z', '+00:00')).replace(second=0, microsecond=0).isoformat()


def get_results(patient) -> List[MCIResult]:
    results_list = []

    if patient.mci.occupation:
        occupation = MCIResult(
            real_date=patient.mci.occupation.at,
            execution_date=round_seconds(patient.mci.occupation.at),
            parameter=ParameterCodes.occupation,
            result=patient.mci.occupation.value
        )
        results_list.append(occupation)
    if patient.mci.transport:
        transport = MCIResult(
            real_date=patient.mci.transport.at,
            execution_date=round_seconds(patient.mci.transport.at),
            parameter=ParameterCodes.transport,
            result=patient.mci.transport.value
        )
        results_list.append(transport)

    for diagnosis in patient.mci.diagnosis:
        for customizer in (diagnosis.customizer or '').split(", "):
            prefix = diagnosis.short_value if diagnosis.short_value is not None else diagnosis.value
            suffix = customizer or ""
            diagnoses = MCIResult(
                real_date=diagnosis.at,
                execution_date=round_seconds(diagnosis.at),
                parameter=ParameterCodes.diagnosis,
                result='-'.join(list(filter(None, [prefix, suffix]))),
            )
            results_list.append(diagnoses)

    for pre_hospital_treatment in patient.mci.pre_hospital_treatment:
        for customizer in (pre_hospital_treatment.customizer or '').split(", "):
            prefix = pre_hospital_treatment.short_value if pre_hospital_treatment.short_value is not None \
                else pre_hospital_treatment.value
            suffix = customizer or ""
            pre_hospital_treatments = MCIResult(
                real_date=pre_hospital_treatment.at,
                execution_date=round_seconds(pre_hospital_treatment.at),
                parameter=ParameterCodes.pre_hospital_treatment,
                result='-'.join(list(filter(None, [prefix, suffix]))),
            )
            results_list.append(pre_hospital_treatments)

    for hospital_treatment in patient.mci.hospital_treatment:
        for customizer in (hospital_treatment.customizer or '').split(", "):
            prefix = hospital_treatment.short_value if hospital_treatment.short_value is not None \
                else hospital_treatment.value
            suffix = customizer or ""
            hospital_treatments = MCIResult(
                real_date=hospital_treatment.at,
                execution_date=round_seconds(hospital_treatment.at),
                parameter=ParameterCodes.hospital_treatment,
                result='-'.join(list(filter(None, [prefix, suffix]))),
            )
            results_list.append(hospital_treatments)

    for imaging in patient.mci.imaging:
        for customizer in (imaging.customizer or '').split(", "):
            prefix = imaging.short_value if imaging.short_value is not None else imaging.value
            suffix = customizer or ""
            imagings = MCIResult(
                real_date=imaging.at,
                execution_date=round_seconds(imaging.at),
                parameter=ParameterCodes.imaging,
                result='-'.join(list(filter(None, [prefix, suffix]))),
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

DELETED_RESULT = 'DELETED'

def process_results(
        results: List[MCIResult],
        previous_results: List[GetDataQueryResponsePatientMCIResult],
        safety_buffer: int
) -> Tuple[List[MCIResult], List[MCIResult]]:
    results_for_chameleon = []
    stored_results = [MCIResult(**previous_result.model_dump()) for previous_result in previous_results]
    threshold = (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=safety_buffer)).isoformat()

    for i in range(len(stored_results)):
        stored_result = stored_results[i]
        if stored_result.result == DELETED_RESULT:
            continue
        if any(result for result in results if
               (result.real_date, result.parameter, result.result) ==
               (stored_result.real_date, stored_result.parameter, stored_result.result)):
            continue
        stored_results[i] = stored_result.copy(update={'result': DELETED_RESULT})
        results_for_chameleon.append(stored_results[i])

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
        previous_result.parameter == result_for_chameleon.parameter and
        result_for_chameleon.result != DELETED_RESULT
    ] for previous_result in previous_results]), problems
    return stored_results, results_for_chameleon


async def write_to_ensemble(patient, results):
    async with aiohttp.ClientSession() as session:
        ret = await session.post(f"{config.ensemble_url}", verify_ssl=False, json={
            "User": config.chameleon_user,
            "Password": config.chameleon_pass,
            "IdNum": patient.info.id_,
            "Patient": patient.info.patient,
            "MedicalRecord": patient.external_id.replace('mci#', ''),
            "Results": [{
                'ExecutionDate': to_mssql_date(r.execution_date),
                'Parameter': r.parameter,
                'Result': r.result
            } for r in results]
        }, auth=BasicAuth(login=config.ensemble_user, password=config.ensemble_pass))
        logger.debug('GOT: {}', await ret.text())
        ret.raise_for_status()


async def mci_data(safety_buffer: int):
    all_results_for_chameleon = []
    for patient in (await GetData.run_query(config.graphql_url, {
        'getPatients(department: "mci")': GetDataQueryResponsePatients,
    })).getPatients.patients:
        try:
            if patient.source_identity == MCI_MANUAL_IDENTITY:
                continue

            results = get_results(patient)
            stored_results, results_for_chameleon = process_results(results, patient.mci_results, safety_buffer)

            await post_dal_json("/mci/mci_to_mongo",
                                json_payload={
                                    'results': [a.model_dump() for a in stored_results],
                                    'external_id': patient.external_id
                                })
            if results_for_chameleon:
                await write_to_ensemble(patient, results_for_chameleon)

            all_results_for_chameleon += results_for_chameleon

        except:
            logger.exception("Could not update Patient {0}".format(patient.info.id_))

    return all_results_for_chameleon
