import datetime
from typing import List, Optional

import logbook
from fastapi import APIRouter, Body
from starlette.responses import FileResponse

from backend import config
from backend.logics.utils import fetch_dal_json, post_dal_json
from common.graphql.graphql import GraphQLQuery, GraphQLModel
from common.data_models.person import Person
from common.mci import MCI_NAMES, MCIIntakeWing, MCI_DEPARTMENT
from common.data_models.patient import Patient
from common.data_models.admission import Admission

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


class GetDataQueryResponsePatientMCIField(GraphQLModel):
    key: str
    value: str
    at: str


class GetDataQueryResponsePatient(GraphQLModel):
    info: GetDataQueryResponsePatientInfo
    admission: GetDataQueryResponsePatientAdmission
    mci: List[GetDataQueryResponsePatientMCIField]


class GetDataQueryResponsePatients(GraphQLModel):
    patients: List[GetDataQueryResponsePatient]


class GetData(GraphQLQuery):
    getPatients: GetDataQueryResponsePatients


@mci_router.get('/export')
async def get_data():
    options = {option['key']: option['name'] for option in
               next(v['options'] for v in await fetch_dal_json("/mci/form") if v['key'] == 'diagnosis')}
    path = f'{datetime.datetime.now().isoformat().replace(":", "-").replace("+", "")}.csv'
    data = '\uFEFFid, name, arrival, location, mechanism\n'
    for patient in (await GetData.run_query(config.graphql_url, {
        'getPatients(department: "mci")': GetDataQueryResponsePatients,
    })).getPatients.patients:
        wing = MCI_NAMES.get(
            MCIIntakeWing[patient.admission.wing_id]) if patient.admission.wing_id != 'wingless' else 'קליטה'
        data += (f'{patient.info.id_}, {patient.info.name}, '
                 f'{datetime.datetime.fromisoformat(patient.admission.arrival).strftime("%d %m %Y - %H %M")},'
                 f'{wing}, {" ".join([options[v.key] for v in patient.mci if v.key in options and v.value != "false"])}\n')
    with open(path, 'w') as dst:
        dst.write(data)
    return FileResponse(path)


@mci_router.post('/patient')
async def create_anonymous_patient(arrival: str = Body(..., embed=True),
                                   wing: Optional[str] = Body(default=None, embed=True)):
    from faker import Faker
    faker = Faker('he-IL')
    external_id = f"mci#{arrival}"
    patient = Patient(
        version=0,
        source_identity='manually',
        external_id=external_id,
        info=Person(
            id_=f'000000{faker.pyint() % 1000:03}',
            name=f"{faker.word()} {faker.color_name()}"
        ),
        admission=Admission(
            arrival=arrival,
            department_id=MCI_DEPARTMENT,
            wing_id=wing
        )
    )

    return await post_dal_json("/mci/patient", json_payload={'patient': patient.model_dump(exclude_unset=True)})


@mci_router.post('/{anonymous_patient}/merge')
async def merge_with_existing_patient(anonymous_patient: str, patient_id: str = Body(..., embed=True)):
    await post_dal_json('/mci/merge', json_payload={"anonymous": anonymous_patient, "patient": patient_id})


@mci_router.post('/unmerge')
async def unmerge_mci_patient(patient_id: str = Body(..., embed=True)):
    await post_dal_json('/mci/unmerge', json_payload={"patient_id": patient_id})
