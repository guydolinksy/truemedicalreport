from pymongo import MongoClient

from . import config


def mongo_client() -> MongoClient:
    return MongoClient(config.mongo_connection)
