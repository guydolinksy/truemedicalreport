from datetime import datetime

import aiohttp
import pytz

from .. import config


def calculate_patient_age(birthdate) -> str:
    stringify_age: str
    try:
        date_diff = datetime.utcnow() - birthdate
        stringify_age = f"{int(date_diff.days / 365)}.{int((date_diff.days % 365) / 30)}"
    except TypeError:
        stringify_age = ""
    return stringify_age


def datetime_utc_serializer(datetime_object):
    serialized: str | None
    try:
        serialized = pytz.timezone('Asia/Jerusalem').localize(datetime_object).isoformat()
    except AttributeError:
        serialized = None
    return serialized


async def post_dal_json(endpoint: str, json_payload: dict) -> dict:
    assert endpoint.startswith("/")

    async with aiohttp.ClientSession() as session:
        ret = await session.post(f"{config.dal_url}{endpoint}", json=json_payload)
        ret.raise_for_status()
        return await ret.json()

async def fetch_dal_json(endpoint: str) -> dict:
    assert endpoint.startswith("/")

    async with aiohttp.ClientSession() as session:
        ret = await session.get(f"{config.dal_url}{endpoint}")
        ret.raise_for_status()
        return await ret.json()

