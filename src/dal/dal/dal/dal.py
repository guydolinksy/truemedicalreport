import datetime
import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

import logbook
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.database import Database

from common.data_models.awaiting import Awaiting, AwaitingTypes
from common.data_models.event import Event
from common.data_models.image import Image, ImagingStatus
from common.data_models.labs import Laboratory, LabCategory, StatusInHebrew, LabStatus
from common.data_models.measures import Measure, MeasureType, FullMeasures, Latest, ExpectedEffect, MeasureEffect
from common.data_models.medicine import Medicine
from common.data_models.notification import Notification
from common.data_models.patient import Patient, ExternalPatient, InternalPatient, PatientInfo, Intake
from common.data_models.referrals import Referral
from common.data_models.treatment import Treatment
from common.data_models.wing import WingFilter, WingFilters, PatientNotifications, WingDetails
from common.utilities.exceptions import PatientNotFound
from common.utilities.websocket import atomic_update
from ..routes.websocket import notify, notify_property

logger = logbook.Logger(__name__)


class Action(Enum):
    insert = 0
    remove = 1
    update = 2


@dataclass
class MedicalDal:
    db: Database

    @property
    def atomic_update_patient(self):
        return atomic_update(klass=Patient, collection=self.db.patients,
                             notify=notify, notify_property=notify_property)

    @property
    def atomic_update_referral(self):
        return atomic_update(klass=Referral, collection=self.db.referrals,
                             notify=notify, notify_property=notify_property)

    @property
    def atomic_update_notification(self):
        return atomic_update(klass=Notification, collection=self.db.notifications,
                             notify=notify, notify_property=notify_property)

    def get_department_wings(self, department: str) -> dict:
        return json.loads(dumps(self.db.wings.find({"department": department}, {"_id": 1, "key": 1, "name": 1})))

    def get_wing(self, department: str, wing: str) -> WingDetails:
        return WingDetails(**self.db.wings.find_one({"department": department, "key": wing}))

    def get_wing_patients(self, department: str, wing: str) -> List[Patient]:
        patients = [Patient(**patient) for patient in
                    self.db.patients.find({"admission.department": department, "admission.wing": wing})]
        return patients

    def get_wing_filters(self, department: str, wing: str) -> WingFilters:
        names = {
            AwaitingTypes.doctor.value: 'צוות רפואי',
            AwaitingTypes.nurse.value: 'צוות סיעודי',
            AwaitingTypes.imaging.value: 'בדיקות הדמייה',
            AwaitingTypes.laboratory.value: 'בדיקות מעבדה',
            AwaitingTypes.referral.value: 'הפניות וייעוצים',
        }
        awaitings, doctors, treatments = {}, {}, {}
        patients = self.get_wing_patients(department, wing)
        for patient in patients:
            for awaiting in patient.awaiting:
                for key, data in patient.awaiting[awaiting].items():
                    if not data.completed:
                        awaitings.setdefault((awaiting, names[awaiting]), {}).setdefault((data.subtype, data.name),
                                                                                         []).append(patient.oid)
            for doctor in patient.treatment.doctors:
                doctors.setdefault(doctor, []).append(patient.oid)
            if patient.treatment.destination:
                treatments.setdefault(patient.treatment.destination, []).append(patient.oid)
        doctor_total = set(p for patients in doctors.values() for p in patients)
        treatment_total = set(p for patients in treatments.values() for p in patients)
        awaiting_total = set(p for keys in awaitings.values() for l in keys.values() for p in l)
        return WingFilters(
            doctors=[
                        WingFilter(
                            key='.'.join(['physician', doctor]), count=len(patients), title=doctor, valid=True,
                            icon='doctor',
                        ) for doctor, patients in doctors.items()
                    ] + [
                        WingFilter(
                            key='no-physician', count=len(patients) - len(doctor_total), title='ללא רופא.ה מטפל.ת',
                            valid=False, icon='doctor',
                        ),
                    ],
            treatments=[
                           WingFilter(
                               key='.'.join(['treatment', treatment]), count=len(patients), title=treatment, valid=True,
                               icon='treatment',
                           ) for treatment, patients in treatments.items()
                       ] + [
                           WingFilter(
                               key='no-treatment', count=len(patients) - len(treatment_total), title='ללא החלטה',
                               valid=True, icon='treatment',
                           ),
                       ],
            awaiting=[
                WingFilter(
                    key='awaiting', count=len(awaiting_total), title='ממתינים.ות', valid=True, icon='awaiting',
                    children=[WingFilter(
                        key=awaiting, count=len(set(p for l in keys.values() for p in l)), icon=awaiting,
                        title=awaiting_name, valid=True, children=[WingFilter(
                            key='.'.join([awaiting, key]), count=len(patients), title=key_name, icon=awaiting,
                            valid=True,
                        ) for (key, key_name), patients in keys.items()]
                    ) for (awaiting, awaiting_name), keys in awaitings.items()]
                ), WingFilter(
                    key='not-awaiting', count=len(patients) - len(awaiting_total), title='לא ממתינים.ות',
                    icon='awaiting', valid=False
                ),
            ],
            mapping=dict(
                [
                    ('.'.join(['treatment', treatment]), patients) for treatment, patients in treatments.items()
                ] + [
                    ('no-treatment', list({p.oid for p in patients} - treatment_total)),
                ] + [
                    ('.'.join(['physician', doctor]), patients) for doctor, patients in doctors.items()
                ] + [
                    ('no-physician', list({p.oid for p in patients} - doctor_total)),
                ] + [
                    ('.'.join([awaiting, key]), patients) for (awaiting, awaiting_name), keys in awaitings.items()
                    for (key, key_name), patients in keys.items()
                ] + [
                    (awaiting, list(set(patient for patients in keys.values() for patient in patients)))
                    for (awaiting, awaiting_name), keys in awaitings.items()
                ] + [
                    ('awaiting', list(awaiting_total)),
                    ('not-awaiting', list({p.oid for p in patients} - awaiting_total)),
                ]
            )
        )

    def get_wing_notifications(self, department: str, wing: str) -> List[PatientNotifications]:
        patients = {patient.external_id: patient for patient in self.get_wing_patients(department, wing)}
        notifications = {external_id: [] for external_id in patients}
        for notification in self.db.notifications.find({"patient_id": {'$in': list(notifications)}}):
            notification = Notification(oid=str(notification.pop("_id")), **notification)
            notifications[notification.patient_id].append(notification)

        return sorted([
            PatientNotifications(
                patient=patients[patient],
                notifications=sorted(notifications, key=lambda n: datetime.datetime.fromisoformat(n.at), reverse=True)
            ) for patient, notifications in notifications.items() if
            notifications or patients[patient].flagged
        ], key=lambda pn: (
            bool(pn.patient.flagged),
            datetime.datetime.fromisoformat(pn.at).timestamp() if pn.at else 0
        ), reverse=True)

    def get_department_patients(self, department: str) -> List[Patient]:
        return [Patient(**p) for p in self.db.patients.find({"admission.department": department})]

    def get_patient_images(self, patient: str) -> List[Image]:
        return [Image(oid=str(image.pop("_id")), **image) for image in self.db.images.find({"patient_id": patient})]

    def get_patient_referrals(self, patient: str) -> List[Referral]:
        return [Referral(oid=str(referral.pop("_id")), **referral) for referral in
                self.db.referrals.find({"patient_id": patient})]

    def get_patient_labs(self, patient: str) -> List[Laboratory]:
        return [Laboratory(oid=str(labs.pop("_id")), **labs) for labs in self.db.labs.find({"patient_id": patient})]

    def get_patient(self, patient: dict) -> Patient:
        res = self.db.patients.find_one(patient)
        if not res:
            raise PatientNotFound()
        return Patient(**res)

    def get_patient_info(self, patient: dict) -> PatientInfo:
        patient = self.get_patient(patient)
        events = [Event(content='קבלה למחלקה', at=patient.admission.arrival, key='arrival')]
        visits = []
        return PatientInfo(
            imaging=[Image(**res) for res in self.db.imaging.find({"patient_id": patient.external_id})],
            full_measures=(FullMeasures(
                measures=[Measure(**d) for d in self.db.measures.find({"patient_id": patient.external_id})]
            )),
            labs=[LabCategory(**tube) for tube in self.db.labs.find({"patient_id": patient.external_id})],
            notifications=[Notification(oid=str(n.pop("_id")), **n)
                           for n in self.db.notifications.find({"patient_id": patient.external_id})],
            referrals=[Referral(oid=str(r.pop("_id")), **r)
                       for r in self.db.referrals.find({"patient_id": patient.external_id})],
            events=events,
            visits=visits,
            **patient.dict()
        )

    def get_patient_by_bed(self, department: str, wing: str, bed: str) -> str:
        res = self.db.patients.find_one({
            "admission.department": department,
            "admission.wing": wing,
            "admission.bed": bed
        })
        return str(res.pop('_id')) if res else None

    async def _cascade_delete_patient(self, patient_external_id):
        """
        delete patient and his data from all collections.
        :param patient_external_id: external_id of patient
        """
        logger.debug(f"Cascade Delete for Patient {patient_external_id}")
        self.db.labs.delete_many({"patient_id": patient_external_id})
        self.db.imaging.delete_many({"patient_id": patient_external_id})
        self.db.measures.delete_many({"patient_id": patient_external_id})
        self.db.referrals.delete_many({"patient_id": patient_external_id})
        self.db.notifications.delete_many({"patient_id": patient_external_id})
        self.db.patients.delete_many({"id_": patient_external_id})

    async def upsert_patient(self, previous: Patient, patient: ExternalPatient):
        if previous and not patient:
            self.db.patients.delete_one({"external_id": previous.external_id})
            await self._cascade_delete_patient(previous.external_id)
        elif previous and patient:
            await self.atomic_update_patient(
                {"_id": ObjectId(previous.oid)},
                patient.dict(exclude_unset=True),
            )
        elif not previous and patient:
            await self.atomic_update_patient(
                {"external_id": patient.external_id},
                dict(
                    **patient.dict(exclude_unset=True),
                    **InternalPatient.from_external_patient(patient).dict(exclude_unset=True)
                ),
            )

    async def upsert_measurements(self, patient_id: str, measures: List[Measure]):
        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        for measure in measures:
            match measure.type:
                case MeasureType.pain.value:
                    if not updated.measures.pain.at_ or measure.at_ > updated.measures.pain.at_:
                        updated.measures.pain = Latest(value=int(measure.value), at=measure.at,
                                                       is_valid=measure.is_valid)
                case MeasureType.pulse.value:
                    if not updated.measures.pulse.at_ or measure.at_ > updated.measures.pulse.at_:
                        updated.measures.pulse = Latest(value=int(measure.value), at=measure.at,
                                                        is_valid=measure.is_valid)
                case MeasureType.temperature.value:
                    if not updated.measures.temperature.at_ or measure.at_ > updated.measures.temperature.at_:
                        updated.measures.temperature = Latest(value=measure.value, at=measure.at,
                                                              is_valid=measure.is_valid)
                case MeasureType.saturation.value:
                    if not updated.measures.saturation.at_ or measure.at_ > updated.measures.saturation.at_:
                        updated.measures.saturation = Latest(value=int(measure.value), at=measure.at,
                                                             is_valid=measure.is_valid)
                case MeasureType.systolic.value:
                    if not updated.measures.systolic.at_ or measure.at_ > updated.measures.systolic.at_:
                        updated.measures.systolic = Latest(value=int(measure.value), at=measure.at,
                                                           is_valid=measure.is_valid)
                case MeasureType.diastolic.value:
                    if not updated.measures.diastolic.at_ or measure.at_ > updated.measures.diastolic.at_:
                        updated.measures.diastolic = Latest(value=int(measure.value), at=measure.at,
                                                            is_valid=measure.is_valid)
            self.db.measures.update_one({"external_id": measure.external_id},
                                        {'$set': dict(patient_id=patient_id, **measure.dict())}, upsert=True)

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'measures'}, exclude_unset=True)
        )

    async def upsert_imaging(self, imaging_obj: Image):
        patient = self.get_patient({"external_id": imaging_obj.patient_id})

        updated = patient.copy()
        self.db.imaging.update_one({"external_id": imaging_obj.external_id},
                                   {'$set': imaging_obj.dict()}, upsert=True)
        if imaging_obj.status != ImagingStatus.ordered.value:
            notification = imaging_obj.to_notification()
            self.db.notifications.update_one({"notification_id": notification.notification_id},
                                             {'$set': notification.dict()}, upsert=True)
            await notify('notification', patient.oid)
        updated.awaiting.setdefault(AwaitingTypes.imaging.value, {}).__setitem__(imaging_obj.external_id, Awaiting(
            subtype=imaging_obj.title,
            name=imaging_obj.title,
            since=imaging_obj.at,
            completed=imaging_obj.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value],
            limit=3600,
        ))

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'awaiting'}, exclude_unset=True)
        )

    async def upsert_labs(self, patient_id: str, new_labs: List[Laboratory]):
        labs: Dict[tuple, LabCategory] = {
            c.key: c for c in [LabCategory(**l) for l in self.db.labs.find({"patient_id": patient_id})]
        }
        for lab in new_labs:
            c = labs.setdefault(lab.category_key, LabCategory(
                patient_id=patient_id, at=lab.at, category_id=lab.category_id, category=lab.category_name
            ))
            c.results[str(lab.test_type_id)] = lab
            c.status = StatusInHebrew[min({l.status for l in c.results.values()})]

        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        for lab in labs.values():
            self.db.labs.update_one({"patient_id": patient_id, **lab.query_key},
                                    {'$set': dict(patient_id=patient_id, **lab.dict(exclude={'patient_id'}))},
                                    upsert=True)
            if lab.status == StatusInHebrew[LabStatus.analyzed.value]:
                notification = lab.to_notification()
                self.db.notifications.update_one({"notification_id": notification.notification_id},
                                                 {'$set': notification.dict()}, upsert=True)
                await notify('notification', patient.oid)
            for key, warning in lab.warnings:
                updated.warnings.setdefault(key, warning)

            logger.debug('%%%%%%%%%%%%%%%% {} {}', patient_id, lab.get_instance_id())
            updated.awaiting.setdefault(AwaitingTypes.laboratory.value, {}).__setitem__(lab.get_instance_id(), Awaiting(
                subtype=lab.category,
                name=lab.category,
                since=lab.at,
                completed=lab.status == StatusInHebrew[LabStatus.analyzed.value],
                limit=3600,
            ))
        logger.debug('{} {}', updated.dict(include={'awaiting', 'warnings'}, exclude_unset=True), patient.dict())

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'awaiting', 'warnings'}, exclude_unset=True)
        )

    async def upsert_referral(self, patient_id, previous: Referral, referral: Referral):
        if previous and not referral:
            updated_referral = previous.copy()
            updated_referral.completed = True
            await self.atomic_update_referral(
                {"_id": ObjectId(previous.oid)},
                updated_referral.dict(exclude_unset=True),
            )
            notification = updated_referral.to_notification()
            await self.atomic_update_notification(
                {"notification_id": notification.notification_id},
                notification.dict(exclude_unset=True),
            )
            patient = self.get_patient({"external_id": patient_id})
            updated = patient.copy()
            updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).__setitem__(
                f'referral#{updated_referral.at}', Awaiting(
                    subtype=updated_referral.to,
                    name=updated_referral.to,
                    since=updated_referral.at,
                    completed=updated_referral.completed,
                    limit=3600,
                )
            )
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={'awaiting'}, exclude_unset=True),
            )

        elif previous and referral:
            await self.atomic_update_referral(
                {"_id": ObjectId(previous.oid)},
                referral.dict(exclude_unset=True),
            )
        elif not previous and referral:
            await self.atomic_update_referral(
                {"external_id": referral.external_id},
                referral.dict(exclude_unset=True),
            )
            patient = self.get_patient({"external_id": patient_id})
            updated = patient.copy()
            updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).__setitem__(
                f'referral#{referral.at}', Awaiting(
                    subtype=referral.to,
                    name=referral.to,
                    since=referral.at,
                    completed=referral.completed,
                    limit=3600,
                )
            )
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={'awaiting'}, exclude_unset=True),
            )

    async def upsert_treatment(self, external_id: str, treatment: Treatment):
        patient = self.get_patient({"external_id": external_id})

        updated = patient.copy()
        updated.treatment = treatment

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'treatment'}, exclude_unset=True)
        )

    async def upsert_intake(self, patient_id: str, intake: Intake):
        patient = self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        updated.intake = intake
        if intake.doctor_seen_time:
            updated.awaiting[AwaitingTypes.doctor.value]['exam'].completed = True
        if intake.nurse_description:
            updated.awaiting[AwaitingTypes.nurse.value]['exam'].completed = True

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)},
            updated.dict(include={'intake', 'awaiting'}, exclude_unset=True)
        )

    async def get_medicine_effects(self) -> Dict[str, List[ExpectedEffect]]:
        return {medicine['name']: ExpectedEffect(**medicine['effect']) for medicine in self.db.medicine_effects.find()}

    async def upsert_medicines(self, patient_id: str, medicines: List[Medicine]):
        medicine_effects = await self.get_medicine_effects()
        patient = self.get_patient({"external_id": patient_id})
        updated = patient.copy()
        updated.awaiting.setdefault(AwaitingTypes.nurse.value, {})
        for medicine in medicines:
            awaiting_obj = Awaiting(since=medicine.since,
                                    subtype='הוראות פעילות',
                                    name=f"{medicine.label}-{medicine.dosage}",
                                    completed=bool(medicine.given),
                                    limit=1500)
            updated.awaiting.setdefault(AwaitingTypes.nurse.value, {}).__setitem__(medicine.get_instance_id(),
                                                                                   awaiting_obj)
            if medicine.given:
                for effect in medicine_effects.get(medicine.label, []):
                    measure = updated.measures.get(effect.measure)
                    if not measure.effect.at_ or measure.effect.at_ < medicine.given_:
                        measure.effect = MeasureEffect(kind=effect.kind, label=medicine.description, at=medicine.given)

        await self.atomic_update_patient({"_id": ObjectId(patient.oid)}, updated.dict(include={'awaiting', 'measures'}))
