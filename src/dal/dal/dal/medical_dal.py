import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, AsyncIterable, Tuple

import logbook
import pytz
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from pydantic import BaseModel

from common.data_models.admission import Admission
from common.data_models.awaiting import Awaiting, AwaitingTypes
from common.data_models.base import AtomicUpdate
from common.data_models.bed import Bed
from common.data_models.department import Department
from common.data_models.discussion import Note
from common.data_models.image import Image
from common.data_models.labs import LabCategory
from common.data_models.mci import MCIStringValue, MCIBooleanValue
from common.data_models.measures import Measure, FullMeasures, ExpectedEffect
from common.data_models.medication import Medication
from common.data_models.patient import Patient, Intake, ExternalData
from common.data_models.plugin import PatientInfoPluginDataV1
from common.data_models.protocol import ProtocolItem
from common.data_models.referrals import Referral
from common.data_models.severity import Severity
from common.data_models.status import Status
from common.data_models.watch import WatchKey
from common.data_models.wing import WingFilter, WingFilters, WingDetails, Wing
from common.utilities.exceptions import PatientNotFoundException
from .application_dal import ApplicationDal
from common.mci import MCI_DEPARTMENT, MCIIntakeWing

logger = logbook.Logger(__name__)


def average_date(l):
    dates = [datetime.datetime.fromisoformat(d).timestamp() for d in l if d is not None and d != '']
    return datetime.datetime.fromtimestamp(
        sum(dates) / len(dates), pytz.timezone('Asia/Jerusalem')
    ).isoformat() if dates else None


@dataclass
class MedicalDal:
    db: Database
    settings_db: Database
    application_dal: ApplicationDal

    async def get_protocol_config(self) -> Dict[str, List[ProtocolItem]]:
        return {k: [ProtocolItem(**i) for i in items] for k, items in
                (await self.application_dal.get_config('protocols', {}))['value'].items()}

    async def get_patients(self, query) -> AsyncIterable[Tuple[str, Patient]]:
        async for patient in self.db.patients.find(query):
            yield str(patient.pop('_id')), Patient(**patient)

    async def get_filters(self, patients: Dict[str, Patient]) -> WingFilters:

        names = {
            AwaitingTypes.doctor: "צוות רפואי",
            AwaitingTypes.nurse: "צוות סיעודי",
            AwaitingTypes.imaging: "בדיקות הדמייה",
            AwaitingTypes.laboratory: "בדיקות מעבדה",
            AwaitingTypes.referral: "הפניות וייעוצים",
        }
        awaitings, doctors, treatments, waiting_intake, time_since_arrival = {}, {}, {}, [], {}
        for oid, patient in patients.items():
            for awaiting in patient.awaiting:
                for key, data in patient.awaiting[awaiting].items():
                    if not data.completed_at:
                        awaitings.setdefault((awaiting, names[awaiting]), {}).setdefault(
                            (data.subtype, data.name), []
                        ).append([oid, patient.awaiting[awaiting][key].since])
            for doctor in patient.treatment.doctors:
                doctors.setdefault(doctor, []).append(oid)

            if await patient.awaiting_intake():
                waiting_intake.append(oid)
            if patient.treatment.destination:
                treatments.setdefault(patient.treatment.destination, []).append(oid)
            time_diff = \
                (
                        datetime.datetime.now(tz=pytz.UTC) - datetime.datetime.fromisoformat(patient.admission.arrival)
                ).total_seconds() / 3600
            if time_diff < 1:
                time_since_arrival.setdefault("0-1", []).append(oid)
            elif time_diff < 6:
                time_since_arrival.setdefault("1-6", []).append(oid)
            elif time_diff < 10:
                time_since_arrival.setdefault("6-10", []).append(oid)
            else:
                time_since_arrival.setdefault("10+", []).append(oid)
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
                            key=".".join(['awaiting', awaiting]),
                            count=len(set(p for l in keys.values() for p, _ in l)),
                            icon=awaiting,
                            title=awaiting_name,
                            valid=True,
                            duration=average_date([d for l in keys.values() for _, d in l]),
                            children=[
                                WingFilter(
                                    key=".".join(['awaiting', awaiting, key]),
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
            time_since_arrival=[
                WingFilter(
                    key=".".join(["time_since", time_since.replace('.', '')]),
                    count=len(patients),
                    title=f"ממתינים.ות {time_since} שעות",
                    icon="awaiting"
                )
                for time_since, patients in time_since_arrival.items()
            ],
            mapping=dict(
                [(".".join(["treatment", treatment]), patients) for treatment, patients in treatments.items()]
                + [(".".join(["treatment", "ללא"]), list({oid for oid in patients} - treatment_total))]
                + [(".".join(["physician", doctor]), patients) for doctor, patients in doctors.items()]
                + [(".".join(["physician", "ללא"]), list({oid for oid in patients} - doctor_total))]
                + [
                    (".".join(['awaiting', awaiting, key]), [p for p, _ in patients])
                    for (awaiting, awaiting_name), keys in awaitings.items()
                    for (key, key_name), patients in keys.items()
                ]
                + [
                    (".".join(['awaiting', awaiting]),
                     list(set(patient for patients in keys.values() for patient, _ in patients)))
                    for (awaiting, awaiting_name), keys in awaitings.items()
                ]
                + [
                    ("awaiting", list(awaiting_total)),
                    ("not-awaiting", list({oid for oid in patients} - awaiting_total)),
                ] +
                [("waiting-intake", waiting_intake)]
                + [
                    (".".join(["time_since", time_since]), patients)
                    for time_since, patients in time_since_arrival.items()
                ]
            ),
        )

    async def get_departments(self) -> AsyncIterable[Department]:
        departments = {}
        async for key, patient in self.get_patients({}):
            departments.setdefault(
                patient.admission.department_id, {}
            ).setdefault(
                patient.admission.wing_id, {}
            ).__setitem__(key, patient)

        department_names = {}
        department_indices = {}
        for department in (await self.application_dal.get_config('departments', []))['value']:
            department_names[department['key']] = department['name']
            department_indices[department['key']] = department['index']
        wing_names = {}
        wing_colors = {}
        wing_indices = {}
        for wing in (await self.application_dal.get_config('wings', []))['value']:
            wing_names.setdefault(wing['department'], {}).__setitem__(wing['key'], wing['name'])
            wing_colors.setdefault(wing['department'], {}).__setitem__(wing['key'], wing.get('color'))
            wing_indices.setdefault(wing['department'], {}).__setitem__(wing['key'], wing['index'])

        for department in sorted(
                set(departments) | set(department_names),
                key=lambda d: department_indices.get(d, 0),
                reverse=True
        ):
            yield Department(
                key=department,
                name=department_names.get(department, department),
                patients=(department_patients := {k: v for wing, patients in departments.get(department, {}).items()
                                                  for k, v in patients.items()}),
                wings=sorted([
                    Wing(
                        details=WingDetails(
                            index=wing_indices.get(department, {}).get(wing, 0),
                            key=wing or 'wingless',
                            name=wing_names.get(department, {}).get(wing, wing or 'ללא מחלקה'),
                            department=department,
                            color=wing_colors.get(department, {}).get(wing),
                        ),
                        filters=await self.get_filters(departments.get(department, {}).get(wing, {})),
                        patients=departments.get(department, {}).get(wing, {}),
                        department_patients=department_patients,
                    ) for wing in set(departments.get(department, {})) | set(wing_names.get(department, {}))
                ], key=lambda w: w.details.index, reverse=True)
            )

    async def get_medication_effects(self, medication) -> List[ExpectedEffect]:
        async for medication_effects in self.settings_db.medication_effects.find({'name': medication}):
            yield ExpectedEffect(**medication_effects["effect"])

    async def get_patient(self, patient_query: dict) -> Patient:
        with AtomicUpdate.set_connection(self):
            _, res = await Patient.from_db(patient_query)

        if res:
            return res

        raise PatientNotFoundException()

    async def update_mci_patients(self, patients: List[str]):
        for patient_id in patients:
            with AtomicUpdate.set_connection(self):
                oid, existing_patient = await Patient.from_db({'external_id': patient_id})

                async def _update(patient: Patient):
                    patient.info = existing_patient.info
                    patient.measures = existing_patient.measures
                    patient.labs = existing_patient.labs
                    patient.imaging = existing_patient.imaging

                async def _create():
                    return Patient(
                        version=0,
                        external_id=f'mci#{patient_id}',
                        info=existing_patient.info,
                        admission=Admission(
                            arrival=existing_patient.admission.arrival,
                            department_id=MCI_DEPARTMENT,
                            wing_id=str(MCIIntakeWing.intake.name),
                        )
                    )

            with AtomicUpdate.set_connection(self):
                await Patient.atomic_update({"external_id": f'mci#{patient_id}'}, update=_update, create=_create)

    async def update_patient(self, patient_query: dict, path: List[str], value: Any, type_: str | bool):
        if type_:
            value = {
                'Severity': Severity,
                'WatchKey': WatchKey,
                'MCIBooleanValue': MCIBooleanValue,
                'MCIStringValue': MCIStringValue,
                'Admission': Admission,
            }[type_](**value)

        async def _update(prev):
            obj = prev
            for part in path[:-1]:
                if isinstance(obj, BaseModel):
                    obj = getattr(obj, part)
                elif isinstance(obj, dict):
                    obj = obj[part]
            if isinstance(obj, BaseModel):
                setattr(obj, path[-1], value)
            elif isinstance(obj, dict):
                obj[path[-1]] = value

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update(patient_query, update=_update)

    async def get_patient_info_plugin_data_v1(self, patient_query: dict) -> PatientInfoPluginDataV1:
        with AtomicUpdate.set_connection(self):
            _, res = await Patient.from_db(patient_query)
        if res:
            return PatientInfoPluginDataV1(
                info=res.info,
                medical_record=res.external_id
            )
        raise PatientNotFoundException()

    async def get_bed(self, department: str, wing: str, bed: str) -> Bed:
        with AtomicUpdate.set_connection(self):
            oid, _ = await Patient.from_db({
                "admission.department_id": department, "admission.wing_id": wing, "admission.bed": bed
            })
        return Bed(patient=oid if oid else None)

    async def upsert_admission(self, external_id: str, patient: Optional[ExternalData]):
        async def _update(prev: Patient):
            external_id: str
            prev.info = patient.info
            prev.esi = patient.esi
            prev.admission = patient.admission
            prev.intake.complaint = patient.intake.complaint
            prev.lab_link = patient.lab_link
            prev.medical_summary_link = patient.medical_summary_link

            # prev.ecg_records = patient.ecg_records

        async def _create():
            return Patient(
                version=0,
                external_id=external_id,
                info=patient.info,
                esi=patient.esi,
                admission=patient.admission,
                intake=patient.intake,
                discussion=patient.discussion,
                treatment=patient.treatment,
                lab_link=patient.lab_link,
                medical_summary_link=patient.medical_summary_link,
                ecg_records=patient.ecg_records,
                status=Status.unassigned,
                severity=Severity(value=patient.esi.value, at=patient.esi.at) if patient.esi else None,
                awaiting={
                    AwaitingTypes.doctor: {
                        'exam': Awaiting(subtype='exam', name='בדיקת צוות רפואי',
                                         since=patient.admission.arrival or "",
                                         status='לא בוצעה', limit=1500)
                    },
                    AwaitingTypes.nurse: {
                        'exam': Awaiting(subtype='exam', name='בדיקת צוות סיעודי',
                                         since=patient.admission.arrival or "",
                                         status='לא בוצעה', limit=1500)
                    },
                },
                flagged=False,
            )

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": external_id}, update=_update if patient else None,
                                        create=_create)

    async def upsert_measurements(self, patient_id: str, measures: List[Measure]):
        latest = {measure.type: None for measure in measures}
        for measure in measures:
            if not latest[measure.type] or latest[measure.type].at_ < measure.at_:
                latest[measure.type] = measure

        async def update(patient) -> None:
            for measure in latest:
                if measure not in patient.measures.model_fields:
                    continue
                elif not (cur := getattr(patient.measures, measure)) or latest[measure].at_ > cur.at_:
                    setattr(patient.measures, measure, latest[measure])
            patient.full_measures = FullMeasures.from_measures(measures)

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_imaging(self, patient_id, images: Dict[str, Image]):
        async def update(patient) -> None:
            patient.imaging = images

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_labs(self, patient_id: str, labs: Dict[str, LabCategory]):
        async def update(patient) -> None:
            patient.labs = labs

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_referral(self, patient_id, at, referrals: Dict[str, Referral]):
        async def update(patient) -> None:
            patient.referrals.update(referrals)
            for external_id in set(patient.referrals) - set(referrals):
                patient.referrals[external_id].completed_at = at

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_doctors(self, patient_id: str, doctors: List[str]):
        async def update(patient) -> None:
            patient.treatment.doctors = doctors

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_destination(self, patient_id: str, destination: Optional[str]):
        async def update(patient) -> None:
            patient.treatment.destination = destination

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_intake_nurse(self, patient_id: str, intake: Intake):
        async def update(patient) -> None:
            patient.intake.nurse_seen_time = intake.nurse_seen_time
            patient.intake.nurse_description = intake.nurse_description

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_intake_doctor(self, patient_id: str, intake: Intake):
        async def update(patient) -> None:
            patient.intake.doctor_seen_time = intake.doctor_seen_time

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_discussion(self, patient_id: str, notes: Dict[str, Note]):
        async def update(patient) -> None:
            for note in notes:
                if note not in patient.discussion.notes or patient.discussion.notes[note].at_ < notes[note].at_:
                    patient.discussion.notes[note] = notes[note]

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)

    async def upsert_medications(self, patient_id: str, medications: Dict[str, Medication]):
        async def update(patient) -> None:
            patient.treatment.medications.update(medications)

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update)
