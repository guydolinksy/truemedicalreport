from fastapi import APIRouter

from src.sheba.ingress.tmr_ingress.faker.fake_data.cameleon_main_inserter import ChameleonMainInserter
from src.sheba.ingress.tmr_ingress.faker.fake_data.fake_main import FakeMain

faker_router = APIRouter()

@faker_router.get("/faker/all", tags=["Patient"])
def update_measurements():
    """
    update the measurments of a single patient.
    query from sql insert to mongo
    :param patient_id:
    :return:
    """
    FakeMain().run()
    return