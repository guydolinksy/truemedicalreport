from motor.motor_asyncio import AsyncIOMotorClient

from . import config
from .dal.dal import MedicalDal


def mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(config.mongo_connection)


def medical_dal() -> MedicalDal:
    return MedicalDal(mongo_client().medical)
