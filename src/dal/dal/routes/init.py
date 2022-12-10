from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from ..clients import mongo_client

init_router = APIRouter()

logger = logbook.Logger(__name__)


@init_router.post("/wings")
def init_db(wings: List[Dict] = Body(..., embed=True), mongo: MongoClient = Depends(mongo_client)):
    mongo.drop_database('medical')
    mongo.medical.wings.delete_many({})
    mongo.medical.wings.insert_many(wings)
