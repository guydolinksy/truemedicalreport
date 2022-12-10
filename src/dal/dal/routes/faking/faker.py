from typing import Tuple, Optional, Iterable

from faker.providers import BaseProvider
from fastapi import APIRouter, Depends, Body
from pymongo import MongoClient
from faker import Faker
import itertools as it
import datetime as dt

from common.data_models.admission import Admission
from common.data_models.esi_score import ESIScore
from common.data_models.intake import Intake
from common.data_models.patient import ExternalPatient, Person
from .faker_consts import ER_DEPARTMENT, WINGS_LAYOUT, WING_KEYS, ALL_BEDS
from ...consts import DAL_FAKER_TAG_NAME
from ...clients import mongo_client, medical_dal
from ...dal.dal import MedicalDal

router = APIRouter(tags=[DAL_FAKER_TAG_NAME])
_faker = Faker("he-IL")


class MedicalPropertiesProvider(BaseProvider):
    __provider__ = "medical_properties"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._patient_counter = it.count(start=1)

    def __patient_id(self) -> int:
        return next(self._patient_counter)

    def binary_gender(self) -> str:
        return self.random_element(["male", "female"])

    def esi_score(self) -> int:
        return self.random_int(1, 4)  # inclusive

    def medical_complaint(self) -> str:
        return self.random_element(
            [
                "קוצר נשימה",
                "כאבים בחזה",
                "סחרחורות",
                "חבלת ראש",
                "חבלת פנים",
                "חבלה בגפיים",
                "בחילות ו/או הקאות",
                "כאב ראש",
                "כאב בטן",
                "לאחר התעלפות",
            ]
        )

    def wing_and_bed(self) -> Tuple[str, str]:
        wing_key = self.random_element(WING_KEYS)
        wing_beds = list(filter(bool, it.chain.from_iterable(WINGS_LAYOUT[wing_key]["beds"])))
        bed = self.random_element(wing_beds)
        return wing_key, bed

    def external_patient(self, wing: str, bed: str) -> ExternalPatient:
        patient_birthdate = dt.datetime.combine(
            _faker.date_of_birth(),
            _faker.time_object(),
        ).replace(tzinfo=dt.timezone.utc)

        age_days = (dt.datetime.now(dt.timezone.utc) - patient_birthdate).days
        age_str = f"{int(age_days / 365)}.{int((age_days % 365) / 30)}"

        patient_id = self.__patient_id()

        admitted_at = _faker.past_datetime("-30m").replace(tzinfo=dt.timezone.utc).isoformat()

        return ExternalPatient(
            external_id=patient_id,
            info=Person(
                id_=patient_id,
                name=_faker.name(),
                gender=_faker.binary_gender(),
                birthdate=patient_birthdate.isoformat(),
                age=age_str,
            ),
            esi=ESIScore(
                value=_faker.esi_score(),
                at=admitted_at,
            ),
            admission=Admission(
                department=ER_DEPARTMENT,
                wing=wing,
                bed=bed,
                arrival=admitted_at,
            ),
            intake=Intake(
                complaint=_faker.medical_complaint(),
            ),
        )

    def external_patients(self, count: int) -> Iterable[ExternalPatient]:
        for wing, bed in self.random_choices(ALL_BEDS, count):
            yield self.external_patient(wing, bed)


_faker.add_provider(MedicalPropertiesProvider)


@router.put("/init_with_wings")
def init_db_with_wings(mongo: MongoClient = Depends(mongo_client)) -> None:
    from dal.routes.init import init_db

    init_db(
        wings=[
            {
                "key": wing_key,
                **wing,
            }
            for wing_key, wing in WINGS_LAYOUT.items()
        ],
        mongo=mongo,
    )


@router.post("/patients/admit", description="Admits new patients. Drops the existing ones.")
async def admit_new_patient(
    dal: MedicalDal = Depends(medical_dal),
    count: Optional[int] = Body(20),
) -> None:

    from dal.routes.department import update_admissions

    await update_admissions(
        department=ER_DEPARTMENT,
        admissions=_faker.external_patients(count),
        dal=dal,
    )
