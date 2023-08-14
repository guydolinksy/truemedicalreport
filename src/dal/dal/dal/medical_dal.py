import asyncio
import datetime
from dataclasses import dataclass
from typing import List, Dict, Type, Any, Optional

import logbook
import pytz
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase as Database, AsyncIOMotorCollection as Collection
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from common.data_models.awaiting import Awaiting, AwaitingTypes
from common.data_models.event import Event
from common.data_models.image import Image, ImagingStatus, ImagingTypes
from common.data_models.discussion import Note, Discussion
from common.data_models.labs import LabCategory, LabStatus
from common.data_models.measures import Measure, MeasureType, FullMeasures, Latest, ExpectedEffect, MeasureEffect
from common.data_models.medicine import Medicine
from common.data_models.notification import Notification
from common.data_models.patient import Patient, ExternalPatient, InternalPatient, PatientInfo, Intake
from common.data_models.plugins import PatientInfoPluginDataV1
from common.data_models.protocol import ProtocolValue, ProtocolItem, Protocol
from common.data_models.referrals import Referral
from common.data_models.severity import Severity
from common.data_models.status import Status
from common.data_models.treatment import Treatment
from common.data_models.wing import WingFilter, WingFilters, PatientNotifications, WingDetails
from common.utilities.exceptions import PatientNotFound, MaxRetriesExceeded
from common.utilities.json_utils import json_to_dot_notation
from .application_dal import ApplicationDal
from ..routes.publishing import publish

logger = logbook.Logger(__name__)


def average_date(l):
    dates = [datetime.datetime.fromisoformat(d).timestamp() for d in l if d is not None and d != '']
    return datetime.datetime.fromtimestamp(
        sum(dates) / len(dates), pytz.timezone('Asia/Jerusalem')
    ).isoformat() if dates else None


@dataclass
class MedicalDal:
    db: Database
    application_dal: ApplicationDal

    @staticmethod
    async def publish_property(klass: Type[BaseModel], oid: str, attr: str, old: Any, new: Any) -> None:
        await publish(".".join([klass.__name__, attr]), dict(oid=oid, old=old, new=new))

    async def _atomic_update(
            self, klass: Type[BaseModel], collection: Collection, query: dict, new: dict, delete: dict, max_retries=10
    ) -> None:

        update = json_to_dot_notation(new)
        unset_update = json_to_dot_notation(delete)
        old = None

        for i in range(max_retries):
            old_full = await collection.find_one(query)
            old = json_to_dot_notation(klass(**old_full).dict(include=set(new), exclude_unset=True)) if old_full else {}

            if all(k in old and update[k] == old[k] for k in update) and not unset_update:
                return
            try:
                update_result = await collection.update_one({**query, **old}, {"$set": update, "$unset": unset_update},
                                                            upsert=True)
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

    async def atomic_update_patient(self, query: dict, new: dict, delete: Optional[dict] = None) -> None:
        await self._atomic_update(klass=Patient, collection=self.db.patients, query=query, new=new, delete=delete or {})

    async def atomic_update_referral(self, query: dict, new: dict, delete: Optional[dict] = None):
        await self._atomic_update(klass=Referral, collection=self.db.referrals, query=query, new=new,
                                  delete=delete or {})

    async def atomic_update_notification(self, query: dict, new: dict, delete: Optional[dict] = None):
        await self._atomic_update(klass=Notification, collection=self.db.notifications, query=query, new=new,
                                  delete=delete or {})

    async def get_protocol_config(self) -> Dict[str, List[ProtocolItem]]:
        return {k: [ProtocolItem(**i) for i in items] for k, items in
                (await self.application_dal.get_config('protocols', {}))['value'].items()}

    async def atomic_update_imaging(self, query: dict, new: dict, delete: Optional[dict] = None):
        await self._atomic_update(klass=Image, collection=self.db.imaging, query=query, new=new, delete=delete or {})

    async def get_department_wings(self, department: str) -> List[WingDetails]:
        return [
            WingDetails(**wing)
            for d in (await self.application_dal.get_config('departments', []))['value'] if d['name'] == department
            for wing in d['wings']
        ]

    async def get_wing_details(self, department: str, wing: str) -> WingDetails:
        return next(w for w in await self.get_department_wings(department) if w.key == wing)

    async def get_wing_patients(self, department: str, wing: str) -> List[Patient]:
        patients = [
            Patient(notifications=sorted([
                Notification(oid=str(n.pop("_id")), **n)
                async for n in self.db.notifications.find({"patient_id": patient['external_id']})
            ], key=lambda n: datetime.datetime.fromisoformat(n.at), reverse=True), **patient)
            async for patient in self.db.patients.find({"admission.department": department, "admission.wing": wing})
        ]
        return patients

    async def is_patient_wait_intake(self, patient):
        measures = []
        for measure in patient.measures.dict().values():
            # check if all the values of measure is null
            measures.append(True) if not measure["value"] else measures.append(False)
        return all(measures) and not patient.intake.complaint

    async def get_wing_filters(self, department: str, wing: str) -> WingFilters:
        names = {
            AwaitingTypes.doctor.value: "צוות רפואי",
            AwaitingTypes.nurse.value: "צוות סיעודי",
            AwaitingTypes.imaging.value: "בדיקות הדמייה",
            AwaitingTypes.laboratory.value: "בדיקות מעבדה",
            AwaitingTypes.referral.value: "הפניות וייעוצים",
        }
        awaitings, doctors, treatments, waiting_intake = {}, {}, {}, []
        patients = await self.get_wing_patients(department, wing)
        for patient in patients:
            for awaiting in patient.awaiting:
                for key, data in patient.awaiting[awaiting].items():
                    if not data.completed:
                        awaitings.setdefault((awaiting, names[awaiting]), {}).setdefault(
                            (data.subtype, data.name), []
                        ).append([patient.oid, patient.awaiting[awaiting][key].since])
            for doctor in patient.treatment.doctors:
                doctors.setdefault(doctor, []).append(patient.oid)

            if await self.is_patient_wait_intake(patient):
                waiting_intake.append(patient.oid)
            if patient.treatment.destination:
                treatments.setdefault(patient.treatment.destination, []).append(patient.oid)

        doctor_total = set(p for patients in doctors.values() for p in patients)
        treatment_total = set(p for patients in treatments.values() for p in patients)
        awaiting_total = set(p for keys in awaitings.values() for l in keys.values() for p, _ in l)
        return WingFilters(
            doctors=[
                        WingFilter(
                            key=".".join(["physician", "ללא"]),
                            count=len(patients) - len(doctor_total),
                            title="ללא",
                            valid=False,
                            icon="doctor",
                        ),
                    ] + [
                        WingFilter(
                            key=".".join(["physician", doctor.replace('.', '')]),
                            count=len(patients),
                            title=doctor.replace('.', ''),
                            valid=True,
                            icon="doctor",
                        )
                        for doctor, patients in doctors.items()
                    ],
            treatments=[
                           WingFilter(
                               key=".".join(["treatment", "ללא"]),
                               count=len(patients) - len(treatment_total),
                               title="לא הוחלט",
                               valid=False,
                               icon="treatment",
                           ),
                       ] + [
                           WingFilter(
                               key=".".join(["treatment", treatment.replace('.', '')]),
                               count=len(patients),
                               title=treatment.replace('.', ''),
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
                            count=len(set(p for l in keys.values() for p, _ in l)),
                            icon=awaiting,
                            title=awaiting_name,
                            valid=True,
                            duration=average_date([d for l in keys.values() for _, d in l]),
                            children=[
                                WingFilter(
                                    key=".".join([awaiting, key]),
                                    count=len(patients),
                                    title=key_name,
                                    icon=awaiting,
                                    valid=True,
                                    duration=average_date([d for _, d in patients]),
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
                    title="ממתינים.ות להחלטה",
                    icon="awaiting",
                    valid=False,
                ),
                WingFilter(
                    key='waiting-intake',
                    count=len(waiting_intake),
                    title="אחות ממיינת",
                    icon="awaiting",
                    valid=False
                )
            ],
            mapping=dict(
                [(".".join(["treatment", treatment]), patients) for treatment, patients in treatments.items()]
                + [(".".join(["treatment", "ללא"]), list({p.oid for p in patients} - treatment_total))]
                + [(".".join(["physician", doctor]), patients) for doctor, patients in doctors.items()]
                + [(".".join(["physician", "ללא"]), list({p.oid for p in patients} - doctor_total))]
                + [
                    (".".join([awaiting, key]), [p for p, _ in patients])
                    for (awaiting, awaiting_name), keys in awaitings.items()
                    for (key, key_name), patients in keys.items()
                ]
                + [
                    (awaiting, list(set(patient for patients in keys.values() for patient, _ in patients)))
                    for (awaiting, awaiting_name), keys in awaitings.items()
                ]
                + [
                    ("awaiting", list(awaiting_total)),
                    ("not-awaiting", list({p.oid for p in patients} - awaiting_total)),
                ] +
                [("waiting-intake", waiting_intake)]
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
            return Patient(
                notifications=sorted([
                    Notification(oid=str(n.pop("_id")), **n)
                    async for n in self.db.notifications.find({"patient_id": res['external_id']})
                ], key=lambda n: datetime.datetime.fromisoformat(n.at), reverse=True),
                referrals=await self.get_patient_referrals(res['external_id']),
                **res
            )

        raise PatientNotFound()

    async def get_patient_info(self, patient: dict) -> PatientInfo:
        patient = await self.get_patient(patient)
        events = [Event(content="קבלה למחלקה", at=patient.admission.arrival, key="arrival")]
        visits = []
        return PatientInfo(
            imaging=await self.get_patient_images(patient.external_id),
            full_measures=(
                FullMeasures(
                    measures=[Measure(**d) async for d in self.db.measures.find({
                        "patient_id": patient.external_id,
                        "value": {"$ne": None},
                    })]
                )
            ),
            labs=await self.get_patient_labs(patient.external_id),
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
                             protocol_config: Dict[str, List[ProtocolItem]], at: str):
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
                        protocol=dict(values={}, **protocol),
                    ),
                )
            else:
                severity = {}
                if patient.esi.value != previous.esi.value:
                    severity = dict(severity=Severity(value=patient.esi.value, at=at).dict(exclude_unset=True))
                await self.atomic_update_patient(
                    {"_id": ObjectId(previous.oid)},
                    dict(
                        **patient.dict(exclude_unset=True),
                        protocol=protocol,
                        **severity,
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

            for item in [item for item in patient.protocol.items if item.match(f'measure-{measure.type}')]:
                if item.key not in patient.protocol.values or patient.protocol.values[item.key].at < measure.at:
                    updated.protocol.values[item.key] = ProtocolValue(value=measure.value, at=measure.at)

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"measures", 'protocol'}, exclude_unset=True)
        )

    async def upsert_imaging(self, patient_id, previous: Image, imaging: Image):
        patient = await self.get_patient({"external_id": patient_id})
        updated = patient.copy()
        if imaging and not previous:
            await self.atomic_update_imaging({"external_id": imaging.external_id}, imaging.dict(exclude_unset=True))
            updated.awaiting.setdefault(AwaitingTypes.imaging.value, {}).__setitem__(
                imaging.external_id,
                Awaiting(
                    subtype=imaging.title,
                    name=imaging.title,
                    since=imaging.ordered_at,
                    completed=self._is_imaging_completed(imaging),
                    status=imaging.status_text,
                    limit=3600,
                ),
            )
            for item in [item for item in patient.protocol.items if item.match(f'imaging-{imaging.title}')]:
                if item.key not in patient.protocol.values or patient.protocol.values[item.key].at < imaging.updated_at:
                    updated.protocol.values[item.key] = ProtocolValue(value=imaging.status_text, at=imaging.updated_at)

            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={"awaiting", "protocol"}, exclude_unset=True),
            )
            if imaging.status != ImagingStatus.ordered.value:
                notification = imaging.to_notification()
                await self.db.notifications.update_one(
                    {"notification_id": notification.notification_id}, {"$set": notification.dict()}, upsert=True
                )
                await publish("notification", patient.oid)
        elif previous and not imaging:
            await self.db.imaging.delete_one({"external_id": previous.external_id})
            updated.awaiting.get(AwaitingTypes.imaging.value, {}).pop(previous.external_id)
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={"awaiting"}, exclude_unset=True),
                delete={"awaiting": {AwaitingTypes.imaging.value: {previous.external_id: ""}}}
            )
            if previous.status != ImagingStatus.ordered.value:
                notification = previous.to_notification()
                await self.db.notifications.delete_one({"notification_id": notification.notification_id})
                await publish("notification", patient.oid)
        elif previous and imaging:
            await self.atomic_update_imaging({"external_id": previous.external_id}, imaging.dict(exclude_unset=True))
            updated.awaiting.setdefault(AwaitingTypes.imaging.value, {}).__setitem__(
                imaging.external_id,
                Awaiting(
                    subtype=imaging.title,
                    name=imaging.title,
                    since=imaging.ordered_at,
                    completed=self._is_imaging_completed(imaging),
                    status=imaging.status_text,
                    limit=3600,
                ),
            )
            for item in [item for item in patient.protocol.items if item.match(f'imaging-{imaging.title}')]:
                if item.key not in patient.protocol.values or patient.protocol.values[item.key].at < imaging.updated_at:
                    updated.protocol.values[item.key] = ProtocolValue(value=imaging.status_text, at=imaging.updated_at)

            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)}, updated.dict(include={"awaiting", "protocol"}, exclude_unset=True)
            )

            if imaging.status != ImagingStatus.ordered.value:
                notification = imaging.to_notification()
                await self.db.notifications.update_one(
                    {"notification_id": notification.notification_id}, {"$set": notification.dict()}, upsert=True
                )
                await publish("notification", patient.oid)

    @staticmethod
    def _is_imaging_completed(imaging: Image) -> bool:
        logger.debug(f"{imaging}")
        if imaging.imaging_type == ImagingTypes.xray.value:
            result = imaging.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value,
                                        ImagingStatus.cancelled.value, ImagingStatus.performed.value]
            logger.debug(f"xray - {imaging}")

            return result
        return imaging.status in [ImagingStatus.verified.value, ImagingStatus.analyzed.value,
                                  ImagingStatus.cancelled.value]

    async def upsert_labs(self, patient_id: str, new_categories: Dict[str, LabCategory]):
        patient = await self.get_patient({"external_id": patient_id})
        updated = patient.copy()
        delete = {}
        labs: Dict[tuple, LabCategory] = {
            c.key: c for c in [LabCategory(**l) async for l in self.db.labs.find({"patient_id": patient_id})]
        }
        for c in set(new_categories) | set(labs):
            if c in new_categories:
                cat = new_categories[c]
                await self.db.labs.update_one(
                    {"patient_id": patient_id, **cat.query_key},
                    {"$set": dict(patient_id=patient_id, **cat.dict(exclude={"patient_id"}))},
                    upsert=True,
                )
                for lab in cat.results.values():
                    for item in [item for item in patient.protocol.items if item.match(f'lab-{lab.test_type_id}')]:
                        value, at = \
                            (f'{lab.result} {lab.units}', lab.result_at) if lab.result_at else ('הוזמן', lab.ordered_at)
                        if item.key not in patient.protocol.values or patient.protocol.values[item.key].at < at:
                            updated.protocol.values[item.key] = ProtocolValue(value=value, at=at)

                for notification in cat.to_notifications():
                    await self.db.notifications.update_one(
                        {"notification_id": notification.notification_id}, {"$set": notification.dict()}, upsert=True
                    )
                    logger.info("current time:{} - notification time: {} - {}",
                                datetime.datetime.utcnow(), notification.at, notification.message)
                await publish("notification", patient.oid)

                for key, warning in cat.get_updated_warnings(
                        {key: warning for key, warning in patient.warnings.items() if key.startswith('lab#')}
                ):
                    updated.warnings[key] = warning

                updated.awaiting.setdefault(AwaitingTypes.laboratory.value, {}).__setitem__(
                    cat.key,
                    Awaiting(
                        subtype=cat.category,  # TODO subtype
                        name=cat.category_display_name,
                        since=cat.ordered_at,
                        completed=cat.status == LabStatus.analyzed.value,
                        status={
                            LabStatus.ordered.value: 'הוזמן',
                            LabStatus.collected.value: 'שויכו דגימות',
                            LabStatus.in_progress.value: 'בעבודה',
                            LabStatus.analyzed.value: 'תוצאות',
                        }.get(cat.status, '?'),
                        limit=3600,
                    ),
                )
            else:
                cat = labs[c]
                await self.db.labs.delete_one({"patient_id": patient_id, **cat.query_key})
                updated.awaiting.get(AwaitingTypes.laboratory.value, {}).pop(cat.key)
                delete[cat.key] = ""

        await self.atomic_update_patient({"_id": ObjectId(patient.oid)}, updated.dict(
            include={"awaiting", "warnings", 'protocol'}, exclude_unset=True
        ), delete={"awaiting": {AwaitingTypes.laboratory.value: delete}} if delete else None)

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

            for item in [item for item in patient.protocol.items if item.match(f'referral-{previous.to}')]:
                if item.key not in patient.protocol.values or patient.protocol.values[item.key].at < at:
                    updated.protocol.values[item.key] = ProtocolValue(value='הפנייה נסגרה', at=at)

            updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).__setitem__(
                previous.get_instance_id(),
                Awaiting(
                    subtype=updated_referral.to,
                    name=updated_referral.to,
                    since=updated_referral.at,
                    completed=updated_referral.completed,
                    status='סגורה' if updated_referral.completed else 'פתוחה',
                    limit=3600,
                ),
            )
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={"awaiting", 'protocol'}, exclude_unset=True),
            )

        elif referral:
            await self.atomic_update_referral(
                {"external_id": referral.external_id},
                referral.dict(exclude_unset=True),
            )
            patient = await self.get_patient({"external_id": patient_id})
            updated = patient.copy()

            for item in [item for item in patient.protocol.items if item.match(f'referral-{referral.to}')]:
                if item.key not in patient.protocol.values or patient.protocol.values[item.key].at < referral.at:
                    updated.protocol.values[item.key] = ProtocolValue(value='הפנייה פתוחה', at=referral.at)

            updated.awaiting.setdefault(AwaitingTypes.referral.value, {}).__setitem__(
                referral.get_instance_id(),
                Awaiting(
                    subtype=referral.to,
                    name=referral.to,
                    since=referral.at,
                    completed=referral.completed,
                    status='סגורה' if referral.completed else 'פתוחה',
                    limit=3600,
                ),
            )
            await self.atomic_update_patient(
                {"_id": ObjectId(patient.oid)},
                updated.dict(include={"awaiting", 'protocol'}, exclude_unset=True),
            )

    async def upsert_treatment(self, external_id: str, update: Treatment):
        patient = await self.get_patient({"external_id": external_id})

        updated = patient.copy()

        treatment = updated.treatment.dict(exclude_unset=True)
        treatment.update(**update.dict(exclude_unset=True))

        updated.treatment = Treatment(**treatment)
        if updated.treatment.destination:
            updated.status = Status.decided.value
        elif updated.treatment.doctors:
            updated.status = Status.undecided.value
        else:
            updated.status = Status.unassigned.value

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"treatment", "status"}, exclude_unset=True)
        )

    async def upsert_intake(self, patient_id: str, intake: Intake):
        patient = await self.get_patient({"external_id": patient_id})

        updated = patient.copy()
        updated.intake = intake
        if intake.doctor_seen_time:
            updated.awaiting[AwaitingTypes.doctor.value]["exam"].completed = True
            updated.awaiting[AwaitingTypes.doctor.value]["exam"].status = 'הושלמה'
        if intake.nurse_description:
            updated.awaiting[AwaitingTypes.nurse.value]["exam"].completed = True
            updated.awaiting[AwaitingTypes.nurse.value]["exam"].status = 'הושלמה'

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"intake", "awaiting"}, exclude_unset=True)
        )

    async def upsert_discussion(self, patient_id: str, notes: Dict[str, Note]):
        patient = await self.get_patient({"external_id": patient_id})

        updated = patient.copy()

        updated.discussion = Discussion(**updated.discussion.dict())

        for id_, note in notes.items():
            if not updated.discussion.notes.get(id_) or updated.discussion.notes.get(id_).at_ < note.at_:
                updated.discussion.notes[id_] = note

        await self.atomic_update_patient(
            {"_id": ObjectId(patient.oid)}, updated.dict(include={"discussion"}, exclude_unset=True)
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
                status='ממתין' if medicine.given else 'ניתן',
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

        await self.atomic_update_patient({"_id": ObjectId(patient.oid)},
                                         updated.dict(include={"awaiting", "measures"}, exclude_unset=True))
