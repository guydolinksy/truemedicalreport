from fastapi import APIRouter

from tmr_ingress.faker.fake_data.fake_main import FakeMain



faker_router = APIRouter()

@faker_router.get("/ingress/faker/all", tags=["Patient"])
def update_measurements():
    """
    update the measurments of a single patient.
    query from sql insert to mongo
    :param patient_id:
    :return:
    """
    FakeMain().run()
    return