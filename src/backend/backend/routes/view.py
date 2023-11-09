from typing import Optional, List

from fastapi import APIRouter

from backend import config

from common.graphql.graphql import GraphQLModel, GraphQLQuery

view_router = APIRouter()


class GetViewsQueryResponseInfo(GraphQLModel):
    id_: str
    name: str
    gender: Optional[str]


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


class GetViewFiltersQueryResponseWatchKey(GraphQLModel):
    update_at: Optional[str]
    triggered: bool
    watched: bool
    message: Optional[str]


class GetViewFiltersQueryResponsePatientInfo(GraphQLModel):
    gender: Optional[str]
    name: str


class GetViewFiltersQueryResponsePatientNotification(GraphQLModel):
    key: str
    static_id: str
    at: str
    link: Optional[str]
    level: str
    type_: str
    message: str
    danger: Optional[bool]


class GetViewFiltersQueryResponsePatientAdmission(GraphQLModel):
    arrival: str
    bed: Optional[str]


class GetViewFiltersQueryResponsePatientSeverity(GraphQLModel):
    value: str


class GetViewFiltersQueryResponsePatient(GraphQLModel):
    oid: str
    flagged: bool
    watching: List[GetViewFiltersQueryResponseWatchKey]
    info: GetViewFiltersQueryResponsePatientInfo
    notifications: List[GetViewFiltersQueryResponsePatientNotification]
    severity: Optional[GetViewFiltersQueryResponsePatientSeverity]
    admission: GetViewFiltersQueryResponsePatientAdmission
    status: str


class XXXXXXX(GraphQLModel):
    flex: Optional[str]
    height: Optional[str]


class GetViewFiltersQueryResponseFiltersItem(GraphQLModel):
    key: str
    icon: str
    count: int
    title: str
    duration: Optional[str]
    valid: bool
    parent: Optional[str]


class GetViewFiltersQueryResponseFiltersMapping(GraphQLModel):
    key: str
    values: List[str]


class GetViewFiltersQueryResponseViewFilters(GraphQLModel):
    doctors: List[GetViewFiltersQueryResponseFiltersItem]
    awaiting: List[GetViewFiltersQueryResponseFiltersItem]
    treatments: List[GetViewFiltersQueryResponseFiltersItem]
    time_since_arrival: List[GetViewFiltersQueryResponseFiltersItem]
    mapping: List[GetViewFiltersQueryResponseFiltersMapping]


class GetViewFiltersQueryResponseViewFiltersResult(GraphQLModel):
    filters: List[GetViewFiltersQueryResponseViewFilters]


class GetViewFiltersQueryResponsePatientsResult(GraphQLModel):
    patients: List[GetViewFiltersQueryResponsePatient]


class GetViewFilters(GraphQLQuery):
    getViewFilters: GetViewFiltersQueryResponseViewFiltersResult
    getPatients: GetViewFiltersQueryResponsePatientsResult


@view_router.get('/{type_}/{key}/filters')
async def get_view_filters(type_: str, key: str) -> GetViewFilters:
    return await GetViewFilters.run_query(config.graphql_url, {
        f'getViewFilters(view_type: "{type_}", key: "{key}")': GetViewFiltersQueryResponseViewFiltersResult,
        f'getPatients(view_type: "{type_}", view: "{key}")': GetViewFiltersQueryResponsePatientsResult,
    })


class GetViewNotificationsQueryResponsePatientNotification(GraphQLModel):
    key: str
    static_id: str
    at: str
    link: Optional[str]
    level: str
    type_: str
    message: str
    danger: Optional[bool]


class GetViewNotificationsQueryResponsePatient(GraphQLModel):
    notifications: List[GetViewNotificationsQueryResponsePatientNotification]


class GetViewNotificationsQueryResponsePatients(GraphQLModel):
    patients: List[GetViewNotificationsQueryResponsePatient]


class GetViewNotifications(GraphQLQuery):
    getPatients: GetViewNotificationsQueryResponsePatients


@view_router.get('/{type_}/{key}/notifications')
async def get_view_notifications(type_: str, key: str) -> GetViewNotifications:
    return await GetViewNotifications.run_query(config.graphql_url, {
        'getViews': GetViewsQueryResponseViews,
        'getDepartments': GetViewsQueryResponseDepartments,
        'getWings': GetViewsQueryResponseWings,
        'getPatients': GetViewsQueryResponsePatients,
    })
