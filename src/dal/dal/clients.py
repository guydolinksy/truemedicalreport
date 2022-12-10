from pymongo import MongoClient

from . import config
from .dal.dal import MedicalDal  # TODO too much nesting, move this out


def mongo_client() -> MongoClient:
    return MongoClient(config.mongo_connection)


def medical_dal() -> MedicalDal:
    return MedicalDal(mongo_client().medical)
