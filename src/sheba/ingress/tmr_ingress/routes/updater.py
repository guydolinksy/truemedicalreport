import asyncio

from fastapi import APIRouter, Body, Depends
from ..updater.update_dal.sql_to_dal import SqlToDal
from ..updater.data_query_booststrap.data_query import DataQuery

updater_router = APIRouter()


def dal_updater() -> SqlToDal:
    return SqlToDal(DataQuery(host="chameleon-db", port=1433, username="su", password="Password123"))


@updater_router.post("/{patient}/measurement", tags=["Patient"])
def update_measurements(patient_id: str, dal: SqlToDal = Depends(dal_updater)):
    """
    update the measurments of a single patient.
    query from sql insert to mongo
    :param patient_id:
    :return:
    """
    return {}


@updater_router.post("/{wing}", tags=["Wing"])
def load_patients_in_wing(wing: str, dal: SqlToDal = Depends(dal_updater)):
    """
    query all the patients in single wing from *Chameleon* and insert it to mongo
    :param wing: wing identifier in Chameleon
    :return:
    """
    return {}


@updater_router.post("/esi_score")
def update_esi_score(wing, dal: SqlToDal = Depends(dal_updater)):
    """
    update the esi score of all the patients
    """
    return dal.get_esi_score()
