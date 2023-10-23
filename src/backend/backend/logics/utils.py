import aiohttp
import logbook
from typing import List

from .. import config

logger = logbook.Logger(__name__)


def prepare_update_object(path: List[str], value: any) -> dict:
    if not path:
        return value

    return {path[0]: prepare_update_object(path[1:], value)}


async def fetch_dal_json(endpoint: str) -> dict:
    assert endpoint.startswith("/")

    async with aiohttp.ClientSession() as session:
        ret = await session.get(f"{config.dal_url}{endpoint}")
        ret.raise_for_status()
        return await ret.json()


async def post_dal_json(endpoint: str, json_payload: dict) -> dict:
    assert endpoint.startswith("/")

    async with aiohttp.ClientSession() as session:
        ret = await session.post(f"{config.dal_url}{endpoint}", json=json_payload)
        ret.raise_for_status()
        return await ret.json()
