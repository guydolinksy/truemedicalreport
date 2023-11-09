from typing import Optional, Dict, Type

import aiohttp
import logbook
from fastapi import HTTPException
from pydantic import BaseModel

logger = logbook.Logger(__name__)


class GraphQLModel(BaseModel):
    @staticmethod
    def are_args_graphql_model(args):
        if len(args) == 0:
            return False
        try:
            if issubclass(args[0], GraphQLModel):
                return True
        except TypeError:
            return False

    @classmethod
    def to_graphql(cls):
        yield '{\n'
        for key, info in cls.model_fields.items():
            yield f'{key}'
            if hasattr(info.annotation, '__args__'):
                # logger.debug('{} {}', info.annotation, info.annotation.__args__)
                if cls.are_args_graphql_model(info.annotation.__args__):
                    yield from info.annotation.__args__[0].to_graphql()
            elif issubclass(info.annotation, GraphQLModel):
                yield from info.annotation.to_graphql()
            yield f'\n'
        yield '}\n'


class GraphQLQuery(BaseModel):

    @classmethod
    async def run_query(cls, connection: str, queries: Dict[str, Type[GraphQLModel]]):
        gql = {q: "".join(r.to_graphql()) for q, r in queries.items()}
        query = 'query {' + '\n'.join([f'{q}{r}' for q, r in gql.items()]) + '}'
        logger.debug('QUERY: {}', query)
        async with aiohttp.ClientSession() as session:
            ret = await session.post(f'{connection}/query', json=dict(query=query))
            ret.raise_for_status()
            result, status = await ret.json()
            if status != 200 or result.get('errors'):
                raise HTTPException(status_code=500, detail='\n'.join([e['message'] for e in result.get('errors', [])]))
            return cls(**result['data'])
