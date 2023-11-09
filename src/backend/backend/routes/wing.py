from typing import List, Optional

import logbook
from fastapi import APIRouter, Depends

from .auth import login_manager
from .. import config
from common.graphql.graphql import GraphQLModel, GraphQLQuery

wing_router = APIRouter()

logger = logbook.Logger(__name__)


class GetWingQueryResponseWingLayout(GraphQLModel):
    beds: List[Optional[str]]
    columns: Optional[str]
    rows: Optional[str]


class GetWingQueryResponseWingDetails(GraphQLModel):
    layout: Optional[GetWingQueryResponseWingLayout]


class GetWingQueryResponseWing(GraphQLModel):
    details: GetWingQueryResponseWingDetails


class GetWingQueryResponseWings(GraphQLModel):
    wings: List[GetWingQueryResponseWing]


class GetWing(GraphQLQuery):
    getWings: GetWingQueryResponseWings


@wing_router.get("/{wing}/layout")
async def get_wing_details(department: str, wing: str, _=Depends(login_manager)) -> GetWing:
    return await GetWing.run_query(config.graphql_url, {
        f'getWings(department: "{department}", key: "{wing}")': GetWingQueryResponseWings,
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
