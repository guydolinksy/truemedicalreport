from typing import List, Dict

import logbook
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient

from .. import config

init_router = APIRouter()

logger = logbook.Logger(__name__)


def client() -> MongoClient:
    return MongoClient(config.mongo_connection)


@init_router.post("/wings")
def init_db(wings: List[Dict] = Body(..., embed=True), dal: MongoClient = Depends(client)):
    dal.drop_database('medical')
    dal.medical.wings.delete_many({})
    dal.medical.wings.insert_many(wings)
