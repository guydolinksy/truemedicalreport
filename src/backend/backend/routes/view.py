from typing import Optional, List

from fastapi import APIRouter

from backend import config

from common.graphql.graphql import GraphQLModel, GraphQLQuery

view_router = APIRouter()


class GetViewsQueryResponseInfo(GraphQLModel):
    id_: str
    name: str
    gender: str


class GetViewsQueryResponseViewMode(GraphQLModel):
    key: str
    name: str
    short_name: str


class GetViewsQueryResponseViewPatient(GraphQLModel):
    oid: str


class GetViewsQueryResponseView(GraphQLModel):
    type: str
    key: str
    name: str
    short_name: str
    department_id: Optional[str]
    wing_id: Optional[str]
    color: Optional[str]
    patients_count: int
    patients: List[GetViewsQueryResponseViewPatient]
    modes: List[GetViewsQueryResponseViewMode]
    default_mode: GetViewsQueryResponseViewMode


class GetViewsQueryResponseDepartment(GraphQLModel):
    key: str
    name: str
    short_name: str


class GetViewsQueryResponseWing(GraphQLModel):
    key: str
    department: str
    name: str
    patients_count: int


class GetViewsQueryResponsePatient(GraphQLModel):
    oid: str
    comment: Optional[str]
    info: GetViewsQueryResponseInfo


class GetViewsQueryResponseViews(GraphQLModel):
    views: List[GetViewsQueryResponseView]


class GetViewsQueryResponseDepartments(GraphQLModel):
    departments: List[GetViewsQueryResponseDepartment]


class GetViewsQueryResponseWings(GraphQLModel):
    wings: List[GetViewsQueryResponseWing]


class GetViewsQueryResponsePatients(GraphQLModel):
    patients: List[GetViewsQueryResponsePatient]


class GetViews(GraphQLQuery):
    getViews: GetViewsQueryResponseViews
    getDepartments: GetViewsQueryResponseDepartments
    getWings: GetViewsQueryResponseWings
    getPatients: GetViewsQueryResponsePatients


@view_router.get('/')
async def get_views() -> GetViews:
    return await GetViews.run_query(config.graphql_url, {
        'getViews': GetViewsQueryResponseViews,
        'getDepartments': GetViewsQueryResponseDepartments,
        'getWings': GetViewsQueryResponseWings,
        'getPatients': GetViewsQueryResponsePatients,
    })
