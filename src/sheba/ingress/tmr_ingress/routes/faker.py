from fastapi import APIRouter

from ..faker.fake_data.fake_main import FakeMain

faker_router = APIRouter()


@faker_router.get("/patient", tags=["Patient"])
def update_measurements():
    """
    update the measurements of a single patient.
    query from sql insert to mongo
    :param patient_id:
    :return:
    """
    FakeMain().insert_new_patient()
    return
