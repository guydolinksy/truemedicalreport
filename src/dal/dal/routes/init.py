from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body

from ..clients import mongo_client, AsyncIOMotorClient

init_router = APIRouter()

logger = logbook.Logger(__name__)


@init_router.post("/wings")
async def init_db(wings: List[Dict] = Body(..., embed=True), mongo: AsyncIOMotorClient = Depends(mongo_client)):
    await mongo.drop_database('medical')
    await mongo.medical.wings.delete_many({})
    await mongo.medical.wings.insert_many(wings)
