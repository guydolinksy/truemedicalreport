import pytz
import datetime
from pathlib import Path
from typing import Dict, Optional

import logbook
from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from ariadne import QueryType, make_executable_schema, load_schema_from_path, graphql_sync, \
    snake_case_fallback_resolvers, ObjectType, graphql
from graphql import GraphQLResolveInfo

from dal.clients import medical_dal
from dal.dal.medical_dal import MedicalDal

graphql_router = APIRouter()
logger = logbook.Logger(__name__)

query = QueryType()


@query.field('getViews')
async def resolve_get_views(_, info: GraphQLResolveInfo):
    medical_dal_: MedicalDal = info.context['medical_dal']

    return dict(success=True, views=await medical_dal_.get_views())


@query.field('getDepartments')
async def resolve_get_departments(_, info: GraphQLResolveInfo, key: Optional[str] = None):
    medical_dal_: MedicalDal = info.context['medical_dal']

    return dict(success=True, departments=await medical_dal_.get_departments(key))


@query.field('getWings')
async def resolve_get_wings(_, info: GraphQLResolveInfo, department: Optional[str] = None, key: Optional[str] = None):
    medical_dal_: MedicalDal = info.context['medical_dal']

    return dict(success=True, wings=await medical_dal_.get_wings(department, key))


@query.field('getBed')
async def resolve_get_bed(_, info: GraphQLResolveInfo, department: str, wing: str, bed: str):
    medical_dal_: MedicalDal = info.context['medical_dal']
    return dict(success=True, patient=await medical_dal_.get_bed(department, wing, bed))


@query.field('getPatients')
async def resolve_get_patients(_, info: GraphQLResolveInfo, department: Optional[str] = None,
                               wing: Optional[str] = None, bed: Optional[str] = None, oid: Optional[str] = None):
    medical_dal_: MedicalDal = info.context['medical_dal']
    get_patients_node = next(fn for fn in info.field_nodes if fn.name.value == 'getPatients')
    patients_node = next(s for s in get_patients_node.selection_set.selections if s.name.value == 'patients')
    members = {fn.name.value for fn in patients_node.selection_set.selections}
    ps  = await medical_dal_.get_patients(department, wing, bed, oid, members=members)
    logger.debug('HERE {}', ps)
    return dict(success=True, patients=ps)


wing = ObjectType('Wing')


@wing.field('filters')
async def resolve_wing_filters(parent, info: GraphQLResolveInfo):
    medical_dal_: MedicalDal = info.context['medical_dal']

    return await medical_dal_.get_wing_filters(parent)

type_defs = load_schema_from_path(Path(__file__).parent / "schema.graphql")
schema = make_executable_schema(type_defs, query, wing, snake_case_fallback_resolvers)


@graphql_router.post('/query')
async def query(query: str = Body(..., embed=True), medical_dal_: MedicalDal = Depends(medical_dal)):
    logger.debug(query)
    success, result = await graphql(
        schema,
        context_value=dict(medical_dal=medical_dal_),
        data=dict(query=query)
    )
    return result, 200 if success else 400
