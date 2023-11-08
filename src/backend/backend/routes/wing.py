from typing import List, Optional

import logbook
from fastapi import APIRouter, Depends

from .auth import login_manager
from .. import config
from common.graphql.graphql import GraphQLModel, GraphQLQuery

wing_router = APIRouter()

logger = logbook.Logger(__name__)


class GetWingQueryResponseWatchKey(GraphQLModel):
    update_at: Optional[str]
    triggered: bool
    watched: bool
    message: Optional[str]


class GetWingQueryResponsePatientInfo(GraphQLModel):
    gender: str
    name: str


class GetWingQueryResponsePatientNotification(GraphQLModel):
    key: str
    static_id: str
    at: str
    link: Optional[str]
    level: str
    type_: str
    message: str
    danger: Optional[bool]


class GetWingQueryResponsePatientAdmission(GraphQLModel):
    arrival: str
    bed: Optional[str]


class GetWingQueryResponsePatientSeverity(GraphQLModel):
    value: str


class GetWingQueryResponsePatient(GraphQLModel):
    oid: str
    flagged: bool
    watching: List[GetWingQueryResponseWatchKey]
    info: GetWingQueryResponsePatientInfo
    notifications: List[GetWingQueryResponsePatientNotification]
    severity: Optional[GetWingQueryResponsePatientSeverity]
    admission: GetWingQueryResponsePatientAdmission
    status: str


class GetWingQueryResponseCSSStyle(GraphQLModel):
    flex: Optional[str]
    height: Optional[str]


class GetWingQueryResponseWingLayout(GraphQLModel):
    beds: List[List[Optional[str]]]
    columns: List[GetWingQueryResponseCSSStyle]
    rows: List[GetWingQueryResponseCSSStyle]


class GetWingQueryResponseWingDetails(GraphQLModel):
    layout: Optional[GetWingQueryResponseWingLayout]


class GetWingQueryResponseWingFilterItem(GraphQLModel):
    key: str
    title: str
    count: int
    parent: Optional[str]


class GetWingQueryResponseWingFilterMapping(GraphQLModel):
    key: str
    values: List[str]


class GetWingQueryResponseWingFilters(GraphQLModel):
    doctors: List[GetWingQueryResponseWingFilterItem]
    awaiting: List[GetWingQueryResponseWingFilterItem]
    treatments: List[GetWingQueryResponseWingFilterItem]
    time_since_arrival: List[GetWingQueryResponseWingFilterItem]
    mapping: List[GetWingQueryResponseWingFilterMapping]


class GetWingQueryResponseWing(GraphQLModel):
    details: GetWingQueryResponseWingDetails
    filters: GetWingQueryResponseWingFilters


class GetWingQueryResponseWings(GraphQLModel):
    wings: List[GetWingQueryResponseWing]


class GetWingQueryResponsePatients(GraphQLModel):
    patients: List[GetWingQueryResponsePatient]


class GetWing(GraphQLQuery):
    getWings: GetWingQueryResponseWings
    getPatients: GetWingQueryResponsePatients


@wing_router.get("/{wing}")
async def get_wing_details(department: str, wing: str, _=Depends(login_manager)) -> GetWing:
    return await GetWing.run_query(config.graphql_url, {
        f'getWings(department: "{department}", key: "{wing}")': GetWingQueryResponseWings,
        f'getPatients(department: "{department}", wing: "{wing}")': GetWingQueryResponsePatients,
    })


class GetBedQueryResponse(GraphQLModel):
    patient: Optional[str]


class GetBed(GraphQLQuery):
    getBed: GetBedQueryResponse


@wing_router.get("/{wing}/beds/{bed}")
async def get_patient_by_bed(department: str, wing: str, bed: str, _=Depends(login_manager)) -> GetBed:
    return await GetBed.run_query(config.graphql_url, {
        f'getBed(department: "{department}", wing: "{wing}", bed: "{bed}")': GetBedQueryResponse
    })
