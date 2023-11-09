from typing import List, Optional

from fastapi import APIRouter, Depends

from .. import config
from .auth import login_manager
from .wing import wing_router
from common.graphql.graphql import GraphQLModel, GraphQLQuery

department_router = APIRouter()

department_router.include_router(wing_router, prefix='/{department}/wings')


class GetDepartmentQueryResponseViewFilterItem(GraphQLModel):
    key: str
    icon: str
    count: int
    title: str
    duration: Optional[str]
    valid: bool
    parent: Optional[str]


class GetDepartmentQueryResponseFilterMapping(GraphQLModel):
    key: str
    values: List[str]


class GetDepartmentQueryResponseViewFilters(GraphQLModel):
    key: str
    doctors: List[GetDepartmentQueryResponseViewFilterItem]
    awaiting: List[GetDepartmentQueryResponseViewFilterItem]
    treatments: List[GetDepartmentQueryResponseViewFilterItem]
    time_since_arrival: List[GetDepartmentQueryResponseViewFilterItem]
    mapping: List[GetDepartmentQueryResponseFilterMapping]


class GetDepartmentQueryResponseWing(GraphQLModel):
    key: str
    name: str
    patients_count: int


class GetDepartmentQueryResponseViewFiltersResult(GraphQLModel):
    filters: List[GetDepartmentQueryResponseViewFilters]


class GetDepartmentQueryResponseWingsResult(GraphQLModel):
    wings: List[GetDepartmentQueryResponseWing]


class GetDepartment(GraphQLQuery):
    getWings: GetDepartmentQueryResponseWingsResult
    getViewFilters: GetDepartmentQueryResponseViewFiltersResult


@department_router.get("/{department}")
async def get_department(department: str, _=Depends(login_manager)) -> GetDepartment:
    return await GetDepartment.run_query(config.graphql_url, {
        f'getWings(department: "{department}")': GetDepartmentQueryResponseWingsResult,
        f'getViewFilters(view_type: "wing", department: "{department}")': GetDepartmentQueryResponseViewFiltersResult,
    })
