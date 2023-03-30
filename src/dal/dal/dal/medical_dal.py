import asyncio
import datetime
from dataclasses import dataclass
from typing import List, Dict, Type, Any

import logbook
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase as Database, AsyncIOMotorCollection as Collection
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from common.data_models.awaiting import Awaiting, AwaitingTypes
from common.data_models.event import Event
from common.data_models.image import Image, ImagingStatus, ImagingTypes
from common.data_models.labs import Laboratory, LabCategory, STATUS_IN_HEBREW, LabStatus
from common.data_models.measures import Measure, MeasureType, FullMeasures, Latest, ExpectedEffect, MeasureEffect
from common.data_models.medicine import Medicine
from common.data_models.notification import Notification
from common.data_models.patient import Patient, ExternalPatient, InternalPatient, PatientInfo, Intake
from common.data_models.plugins import PatientInfoPluginDataV1
from common.data_models.protocol import ProtocolValue, ProtocolItem, Protocol
from common.data_models.referrals import Referral
from common.data_models.treatment import Treatment
from common.data_models.wing import WingFilter, WingFilters, PatientNotifications, WingDetails
from common.utilities.exceptions import PatientNotFound, MaxRetriesExceeded
from common.utilities.json_utils import json_to_dot_notation
from .application_dal import ApplicationDal
from ..routes.publishing import publish

logger = logbook.Logger(__name__)


@dataclass
class MedicalDal:
    db: Database
    application_dal: ApplicationDal

    @staticmethod
    async def publish_property(klass: Type[BaseModel], oid: str, attr: str, old: Any, new: Any) -> None:
        await publish(".".join([klass.__name__, attr]), dict(oid=oid, old=old, new=new))

    async def _atomic_update(
            self, klass: Type[BaseModel], collection: Collection, query: dict, new: dict, max_retries=10
    ) -> None:

        update = json_to_dot_notation(new)
        old = None
        old_full = None

        for i in range(max_retries):
            old_full = await collection.find_one(query)
            old = json_to_dot_notation(klass(**old_full).dict(include=set(new), exclude_unset=True)) if old_full else {}

            if all(k in old and update[k] == old[k] for k in update):
                return
            try:
                update_result = await collection.update_one({**query, **old}, {"$set": update}, upsert=True)
                if update_result.modified_count or update_result.upserted_id:
                    break
            except DuplicateKeyError:
                pass
        else:
            raise MaxRetriesExceeded(f"{query}: {old} -> {new}")

        new_full = await collection.find_one(query)

        if oid := str(new_full.pop("_id")):
            for attr in new:
                if old.get(attr) != new.get(attr):
                    await self.publish_property(klass, oid, attr, old.get(attr), new.get(attr))

        if old_full:
            del old_full["_id"]  # Not JSON serializable, and we already have the ObjectId in a separate field

        await publish(klass.__name__, {
            "oid": oid,
            "old": old_full,
            "new": new_full,
        })

    async def atomic_update_patient(self, query: dict, new: dict) -> None:
        await self._atomic_update(klass=Patient, collection=self.db.patients, query=query, new=new)

    async def atomic_update_referral(self, query: dict, new: dict):
        await self._atomic_update(klass=Referral, collection=self.db.referrals, query=query, new=new)

    async def atomic_update_notification(self, query: dict, new: dict):
        await self._atomic_update(klass=Notification, collection=self.db.notifications, query=query, new=new)

    async def get_protocol_config(self) -> Dict[str, List[ProtocolItem]]:
        return {k: [ProtocolItem(**i) for i in items] for k, items in
                (await self.application_dal.get_config('protocols', {})).items()}

    async def get_department_wings(self, department: str) -> List[WingDetails]:
        return [
            WingDetails(**wing)
            for d in await self.application_dal.get_config('departments', []) if d['name'] == department
            for wing in d['wings']
        ]

    async def get_wing_details(self, department: str, wing: str) -> WingDetails:
        return next(w for w in await self.get_department_wings(department) if w.key == wing)

    async def get_wing_patients(self, department: str, wing: str) -> List[Patient]:
        patients = [
            Patient(**patient)
            async for patient in self.db.patients.find({"admission.department": department, "admission.wing": wing})
        ]
        return patients

    async def get_wing_filters(self, department: str, wing: str) -> WingFilters:
        names = {
            AwaitingTypes.doctor.value: "צוות רפואי",
            AwaitingTypes.nurse.value: "צוות סיעודי",
            AwaitingTypes.imaging.value: "בדיקות הדמייה",
            AwaitingTypes.laboratory.value: "בדיקות מעבדה",
            AwaitingTypes.referral.value: "הפניות וייעוצים",
        }
        awaitings, doctors, treatments = {}, {}, {}
        patients = await self.get_wing_patients(department, wing)
        for patient in patients:
            for awaiting in patient.awaiting:
                for key, data in patient.awaiting[awaiting].items():
                    if not data.completed:
                        awaitings.setdefault((awaiting, names[awaiting]), {}).setdefault(
                            (data.subtype, data.name), []
                        ).append(patient.oid)
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
                            key="no-physician",
                            count=len(patients) - len(doctor_total),
                            title="ללא",
                            valid=False,
                            icon="doctor",
                        ),
                    ]
                    + [
                        WingFilter(
                            key=".".join(["physician", doctor]),
                            count=len(patients),
                            title=doctor,
                            valid=True,
                            icon="doctor",
                        )
                        for doctor, patients in doctors.items()
                    ],
            treatments=[
                           WingFilter(
                               key="no-treatment",
                               count=len(patients) - len(treatment_total),
                               title="ללא",
                               valid=True,
                               icon="treatment",
                           ),
                       ]
                       + [
                           WingFilter(
                               key=".".join(["treatment", treatment]),
                               count=len(patients),
                               title=treatment,
                               valid=True,
                               icon="treatment",
                           )
                           for treatment, patients in treatments.items()
                       ],
            awaiting=[
                WingFilter(
                    key="awaiting",
                    count=len(awaiting_total),
                    title="ממתינים.ות",
                    valid=True,
                    icon="awaiting",
                    children=[
                        WingFilter(
                            key=awaiting,
                            count=len(set(p for l in keys.values() for p in l)),
                            icon=awaiting,
                            title=awaiting_name,
                            valid=True,
                            children=[
                                WingFilter(
                                    key=".".join([awaiting, key]),
                                    count=len(patients),
                                    title=key_name,
                                    icon=awaiting,
                                    valid=True,
                                )
                                for (key, key_name), patients in keys.items()
                            ],
                        )
                        for (awaiting, awaiting_name), keys in awaitings.items()
                    ],
                ),
                WingFilter(
                    key="not-awaiting",
                    count=len(patients) - len(awaiting_total),
                    title="לא ממתינים.ות",
                    icon="awaiting",
                    valid=False,
                ),
            ],
            mapping=dict(
                [(".".join(["treatment", treatment]), patients) for treatment, patients in treatments.items()]
                + [
                    ("no-treatment", list({p.oid for p in patients} - treatment_total)),
                ]
                + [(".".join(["physician", doctor]), patients) for doctor, patients in doctors.items()]
                + [
                    ("no-physician", list({p.oid for p in patients} - doctor_total)),
                ]
                + [
                    (".".join([awaiting, key]), patients)
                    for (awaiting, awaiting_name), keys in awaitings.items()
                    for (key, key_name), patients in keys.items()
                ]
                + [
                    (awaiting, list(set(patient for patients in keys.values() for patient in patients)))
                    for (awaiting, awaiting_name), keys in awaitings.items()
                ]
                + [
                    ("awaiting", list(awaiting_total)),
                    ("not-awaiting", list({p.oid for p in patients} - awaiting_total)),
                ]
            ),
        )

    async def get_wing_notifications(self, department: str, wing: str) -> List[PatientNotifications]:
        patients = {patient.external_id: patient for patient in await self.get_wing_patients(department, wing)}
        notifications = {external_id: [] for external_id in patients}
        async for notification in self.db.notifications.find({"patient_id": {"$in": list(notifications)}}):
            notification = Notification(oid=str(notification.pop("_id")), **notification)
            notifications[notification.patient_id].append(notification)

        return sorted(
            [
                PatientNotifications(
                    patient=patients[patient],
                    notifications=sorted(
                        notifications, key=lambda n: datetime.datetime.fromisoformat(n.at), reverse=True
                    ),
                )
                for patient, notifications in notifications.items()
                if notifications or patients[patient].flagged
            ],
            key=lambda pn: (
                bool(pn.patient.flagged),
                datetime.datetime.fromisoformat(pn.at).timestamp() if pn.at else 0,
            ),
            reverse=True,
        )

    async def get_department_patients(self, department: str) -> List[Patient]:
        return [Patient(**p) async for p in self.db.patients.find({"admission.department": department})]

    async def get_patient_images(self, patient: str) -> List[Image]:
        return [
            Image(oid=str(image.pop("_id")), **image) async for image in self.db.imaging.find({"patient_id": patient})
        ]

    async def get_patient_referrals(self, patient: str) -> List[Referral]:
        return [
            Referral(oid=str(referral.pop("_id")), **referral)
            async for referral in self.db.referrals.find({"patient_id": patient})
        ]

    async def get_patient_labs(self, patient: str) -> List[LabCategory]:
        return [
            LabCategory(oid=str(labs.pop("_id")), **labs) async for labs in self.db.labs.find({"patient_id": patient})
        ]

    async def get_patient(self, patient_query: dict) -> Patient:
        if res := await self.db.patients.find_one(patient_query):
            return Patient(notifications=[
                Notification(oid=str(n.pop("_id")), **n)
                async for n in self.db.notifications.find({"patient_id": res['external_id']})
            ], **res)

        raise PatientNotFound()

    async def get_patient_info(self, patient: dict) -> PatientInfo:
        patient = await self.get_patient(patient)
        events = [Event(content="קבלה למחלקה", at=patient.admission.arrival, key="arrival")]
        visits = []
        return PatientInfo(
            imaging=await self.get_patient_images(patient.external_id),
            full_measures=(
                FullMeasures(
                    measures=[Measure(**d) async for d in self.db.measures.find({"patient_id": patient.external_id})]
                )
            ),
            labs=await self.get_patient_labs(patient.external_id),
            referrals=await self.get_patient_referrals(patient.external_id),
            events=events,
            visits=visits,
            **patient.dict(),
        )

    async def get_patient_info_plugin_data_v1(self, patient: dict) -> PatientInfoPluginDataV1:
        patient = await self.get_patient(patient)
        return PatientInfoPluginDataV1(
            info=patient.info,
            medical_record=patient.external_id
        )

    async def get_patient_by_bed(self, department: str, wing: str, bed: str) -> str:
        res = await self.db.patients.find_one(
            {"admission.department": department, "admission.wing": wing, "admission.bed": bed}
        )
        return str(res.pop("_id")) if res else None

    async def _cascade_delete_patient(self, patient_external_id):
        """
        delete patient and their data from all collections.
        :param patient_external_id: external_id of patient
        """
        logger.debug(f"Cascade Delete for Patient {patient_external_id}")
        await asyncio.gather(
            *[
                self.db.patients.delete_one({"external_id": patient_external_id}),
                self.db.labs.delete_many({"patient_id": patient_external_id}),
                self.db.imaging.delete_many({"patient_id": patient_external_id}),
                self.db.measures.delete_many({"patient_id": patient_external_id}),
                self.db.referrals.delete_many({"patient_id": patient_external_id}),
                self.db.notifications.delete_many({"patient_id": patient_external_id}),
                self.db.patients.delete_many({"id_": patient_external_id}),
            ]
        )

    async def upsert_patient(self, previous: Patient, patient: ExternalPatient,
                             protocol_config: Dict[str, List[ProtocolItem]]):
        if previous and not patient:
            await self._cascade_delete_patient(previous.external_id)
            await publish(Patient.__name__, {
                "oid": previous.oid,
                "old": previous.dict(),
            })
            await self.publish_property(Patient, previous.oid, "admission", previous.admission.dict(), None)
        elif patient:
            protocol = Protocol(
                active=patient.intake.complaint in protocol_config,
                items=protocol_config.get(patient.intake.complaint, []),
            ).dict(exclude_unset=True)
            if not previous:
                await self.atomic_update_patient(
                    {"external_id": patient.external_id},
                    dict(
                        **patient.dict(exclude_unset=True),
                        **InternalPatient.from_external_patient(patient).dict(exclude_unset=True),
                        protocol=protocol,
                    ),
                )
            else:
                await self.atomic_update_patient(
                    {"_id": ObjectId(previous.oid)},
                    dict(
                        **patient.dict(exclude_unset=True),
                        protocol=protocol,
                    )
                )

    async def upsert_measurements(self, patient_id: str, measures: List[Measure]):
        patient = await self.get_patient({"external_id": patient_id})
        updated = patient.copy()

        for measure in measures:
            match measure.type:
                case MeasureType.pain.value:
                    if not updated.measures.pain.at_ or measure.at_ > updated.measures.pain.at_:
                        updated.measures.pain = Latest(
                            value=measure.value, at=measure.at,
                            is_valid=measure.is_valid
                        )
                case MeasureType.pulse.value:
                    if not updated.measures.pulse.at_ or measure.at_ > updated.measures.pulse.at_:
                        updated.measures.pulse = Latest(
                            value=measure.value, at=measure.at,
                            is_valid=measure.is_valid
                        )
                case MeasureType.temperature.value:
                    if not updated.measures.temperature.at_ or measure.at_ > updated.measures.temperature.at_:
                        updated.measures.temperature = Latest(
                            value=measure.value, at=measure.at,
                            is_valid=measure.is_valid
                        )
                case MeasureType.saturation.value:
                    if not updated.measures.saturation.at_ or measure.at_ > updated.measures.saturation.at_:
                        updated.measures.saturation = Latest(
                            value=measure.value, at=measure.at,
                            is_valid=measure.is_valid
                        )
                case MeasureType.systolic.value:
                    if not updated.measures.systolic.at_ or measure.at_ > updated.measures.systolic.at_:
                        updated.measures.systolic = Latest(
                            value=measure.value, at=measure.at,
                            is_valid=measure.is_valid
                        )
                case MeasureType.diastolic.value:
                    if not updated.measures.diastolic.at_ or measure.at_ > updated.measures.diastolic.at_:
                        updated.measures.diastolic = Latest(
                            value=measure.value, at=measure.at,
                            is_valid=measure.is_valid
                        )
            await self.db.measures.update_one(
                {"external_id": measure.external_id},
                {"$set": dict(patient_id=patient_id, **measure.dict())},
                upsert=True,
            )
            for key in [k for item in patient.protocol.items for k in item.keys if k == f'measure-{measure.type}']:
                if key not in patient.protocol.values or patient.protocol.values[key].at < measure.at:
                    updated.protocol.values[key] = ProtocolValue(value=measure.value, at=measure.at)

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"measures", 'protocol'}, exclude_unset=True)
        )

    async def upsert_imaging(self, imaging_obj: Image):
        patient = await self.get_patient({"external_id": imaging_obj.patient_id})

        updated = patient.copy()
        await self.db.imaging.update_one(
            {"external_id": imaging_obj.external_id}, {"$set": imaging_obj.dict()}, upsert=True
        )
        if imaging_obj.status != ImagingStatus.ordered.value:
            notification = imaging_obj.to_notification()
            await self.db.notifications.update_one(
                {"notification_id": notification.notification_id}, {"$set": notification.dict()}, upsert=True
            )
            await publish("notification", patient.oid)

        for key in [k for item in patient.protocol.items for k in item.keys
                    if k == f'imaging-{imaging_obj.imaging_type}']:
            # TODO: should be changed to `updated_at` after the imaging bugfix is merged.
            if key not in patient.protocol.values or patient.protocol.values[key].at < imaging_obj.ordered_at:
                updated.protocol.values[key] = ProtocolValue(value=imaging_obj.status_text, at=imaging_obj.ordered_at)

        updated.awaiting.setdefault(AwaitingTypes.imaging.value, {}).__setitem__(
            imaging_obj.external_id,
            Awaiting(
                subtype=imaging_obj.title,
                name=imaging_obj.title,
                since=imaging_obj.accomplished_at if imaging_obj.accomplished_at else imaging_obj.ordered_at,
                completed=self._is_imaging_completed(imaging_obj),
                limit=3600,
            ),
        )

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"awaiting", "protocol"}, exclude_unset=True)
        )

    @staticmethod
    def _is_imaging_completed(imaging: Image) -> bool:
        if imaging.imaging_type == ImagingTypes.xray:
            return imaging.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value,
                                      ImagingStatus.cancelled.value, ImagingStatus.performed.value]
        return imaging.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value]

    async def upsert_labs(self, patient_id: str, new_labs: List[Laboratory]):
        patient = await self.get_patient({"external_id": patient_id})
        updated = patient.copy()

        labs: Dict[tuple, LabCategory] = {
            c.key: c for c in [LabCategory(**l) async for l in self.db.labs.find({"patient_id": patient_id})]
        }
        for lab in new_labs:
            c = labs.setdefault(
                lab.category_key,
                LabCategory(patient_id=patient_id, ordered_at=lab.ordered_at, result_at=lab.result_at,
                            category_id=lab.category_id, category=lab.category_name),
            )
            c.results[str(lab.test_type_id)] = lab
            c.status = STATUS_IN_HEBREW[min({l.status for l in c.results.values()})]

            for key in [k for item in patient.protocol.items for k in item.keys if k == f'lab-{lab.test_type_id}']:
                value, at = (lab.result, lab.result_at) if lab.result_at else ('הוזמן', lab.ordered_at)
                if key not in patient.protocol.values or patient.protocol.values[key].at < at:
                    updated.protocol.values[key] = ProtocolValue(value=value, at=at)

        for lab in labs.values():
            await self.db.labs.update_one(
                {"patient_id": patient_id, **lab.query_key},
                {"$set": dict(patient_id=patient_id, **lab.dict(exclude={"patient_id"}))},
                upsert=True,
            )
            if lab.status == STATUS_IN_HEBREW[LabStatus.analyzed.value]:
                notification = lab.to_notification()
                await self.db.notifications.update_one(
                    {"notification_id": notification.notification_id}, {"$set": notification.dict()}, upsert=True
                )
                logger.info(
                    f"current time:{datetime.datetime.utcnow()} - notification time: {notification.at} - {notification.message}")
                await publish("notification", patient.oid)

            for key, warning in lab.get_updated_warnings(
                    {key: warning for key, warning in patient.warnings.items() if key.startswith('lab#')}
            ):
                updated.warnings[key] = warning

            updated.awaiting.setdefault(AwaitingTypes.laboratory.value, {}).__setitem__(
                lab.get_instance_id(),
                Awaiting(
                    subtype=lab.category,
                    name=lab.category,
                    since=lab.ordered_at,
                    completed=lab.status == STATUS_IN_HEBREW[LabStatus.analyzed.value],
                    limit=3600,
                ),
            )

        await self.atomic_update_patient({"_id": ObjectId(patient.oid)}, updated.dict(
            include={"awaiting", "warnings", 'protocol'}, exclude_unset=True
        ))

    async def upsert_referral(self, patient_id, at, previous: Referral, referral: Referral):
        if previous and not referral:
            updated_referral = previous.copy()
            updated_referral.completed = True
            await self.atomic_update_referral(
                {"external_id": previous.external_id},
                updated_referral.dict(exclude_unset=True),
            )
            notification = updated_referral.to_notification()
            await self.atomic_update_notification(
                {"notification_id": notification.notification_id},
                notification.dict(exclude_unset=True),
            )
            patient = await self.get_patient({"external_id": patient_id})
            updated = patient.copy()

            for key in [k for item in patient.protocol.items for k in item.keys if k == f'referral-{referral.to}']:
                if key not in patient.protocol.values or patient.protocol.values[key].at < at:
                    updated.protocol.values[key] = ProtocolValue(value='הפנייה נסגרה', at=at)

            updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).__setitem__(
                previous.get_instance_id(),
                Awaiting(
                    subtype=updated_referral.to,
                    name=updated_referral.to,
                    since=updated_referral.at,
                    completed=updated_referral.completed,
                    limit=3600,
                ),
            )
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={"awaiting", 'protocol'}, exclude_unset=True),
            )

        elif previous and referral:
            await self.atomic_update_referral(
                {"external_id": previous.external_id},
                referral.dict(exclude_unset=True),
            )
        elif not previous and referral:
            await self.atomic_update_referral(
                {"external_id": referral.external_id},
                referral.dict(exclude_unset=True),
            )
            patient = await self.get_patient({"external_id": patient_id})
            updated = patient.copy()

            for key in [k for item in patient.protocol.items for k in item.keys if k == f'referral-{referral.to}']:
                if key not in patient.protocol.values or patient.protocol.values[key].at < referral.at:
                    updated.protocol.values[key] = ProtocolValue(value='הפנייה פתוחה', at=referral.at)

            updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).__setitem__(
                referral.get_instance_id(),
                Awaiting(
                    subtype=referral.to,
                    name=referral.to,
                    since=referral.at,
                    completed=referral.completed,
                    limit=3600,
                ),
            )
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={"awaiting", 'protocol'}, exclude_unset=True),
            )

    async def upsert_treatment(self, external_id: str, treatment: Treatment):
        patient = await self.get_patient({"external_id": external_id})

        updated = patient.copy()
        updated.treatment = treatment

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"treatment"}, exclude_unset=True)
        )

    async def upsert_intake(self, patient_id: str, intake: Intake):
        patient = await self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        updated.intake = intake
        if intake.doctor_seen_time:
            updated.awaiting[AwaitingTypes.doctor.value]["exam"].completed = True
        if intake.nurse_description:
            updated.awaiting[AwaitingTypes.nurse.value]["exam"].completed = True

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"intake", "awaiting"}, exclude_unset=True)
        )

    async def get_medicine_effects(self) -> Dict[str, List[ExpectedEffect]]:
        return {
            medicine["name"]: ExpectedEffect(**medicine["effect"]) async for medicine in self.db.medicine_effects.find()
        }

    async def upsert_medicines(self, patient_id: str, medicines: List[Medicine]):
        medicine_effects = await self.get_medicine_effects()
        patient = await self.get_patient({"external_id": patient_id})
        updated = patient.copy()
        updated.awaiting.setdefault(AwaitingTypes.nurse.value, {})
        for medicine in medicines:
            awaiting_obj = Awaiting(
                since=medicine.since,
                subtype="הוראות פעילות",
                name=f"{medicine.label}-{medicine.dosage}",
                completed=bool(medicine.given),
                limit=1500,
            )
            updated.awaiting.setdefault(AwaitingTypes.nurse.value, {}).__setitem__(
                medicine.get_instance_id(), awaiting_obj
            )
            if medicine.given:
                for effect in medicine_effects.get(medicine.label, []):
                    measure = updated.measures.get(effect.measure)
                    if not measure.effect.at_ or measure.effect.at_ < medicine.given_:
                        measure.effect = MeasureEffect(kind=effect.kind, label=medicine.description, at=medicine.given)

        await self.atomic_update_patient({"_id": ObjectId(patient.oid)}, updated.dict(include={"awaiting", "measures"}))
