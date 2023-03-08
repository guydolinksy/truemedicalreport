from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from . import config
from .dal.application_dal import ApplicationDal
from .dal.medical_dal import MedicalDal


def mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(config.mongo_connection)


def application_dal() -> ApplicationDal:
    return ApplicationDal(mongo_client().app)


def medical_dal(application_dal_: ApplicationDal = Depends(application_dal)) -> MedicalDal:
    return MedicalDal(db=mongo_client().medical, application_dal=application_dal_)
