import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, AsyncIterable, Tuple, Set

import logbook
import pytz
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase as Database
from pydantic import BaseModel

from common.data_models.admission import Admission
from common.data_models.awaiting import Awaiting, AwaitingTypes
from common.data_models.base import AtomicUpdate
from common.data_models.discussion import Note
from common.data_models.image import Image
from common.data_models.labs import LabCategory
from common.data_models.mci import MCIStringValue, MCIBooleanValue, MCIListItemValue
from common.data_models.measures import Measure, FullMeasures, ExpectedEffect
from common.data_models.medication import Medication
from common.data_models.patient import Patient, Intake, ExternalData
from common.data_models.plugin import PatientInfoPluginDataV1
from common.data_models.protocol import ProtocolItem
from common.data_models.referrals import Referral
from common.data_models.severity import Severity
from common.data_models.status import Status
from common.data_models.watch import WatchKey
from common.mci import MCI_DEPARTMENT, MCI_INTAKE_MAPPING
from common.utilities.exceptions import PatientNotFoundException

from ..routes.trauma import get_records
from .application_dal import ApplicationDal

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

    async def get_patient_admissions(self, query) -> AsyncIterable[Tuple[str, str, Optional[str]]]:
        async for patient in self.db.patients.find(query, {'admission.department_id': 1, 'admission.wing_id': 1}):
            yield str(patient['_id']), patient['admission']['department_id'], patient['admission']['wing_id']

    async def get_views(self) -> List[Dict]:
        admissions = [admission async for admission in self.get_patient_admissions({})]

        view_colors = {}
        for view in (await self.application_dal.get_config('views', []))['value']:
            view_colors[view['key']] = view.get('color')

        views = [dict(
            type='wing',
            key=f"W{w['key']}",
            name=w['name'],
            short_name=w['name'],
            wing_id=w['key'],
            department_id=w['department'],
            patients=w['patients'],
            patients_count=len(w['patients']),
            color=view_colors.get(f"W{w['key']}"),
            modes=[dict(
                key='wing',
                name='תצוגת מטופלים',
                short_name='מטופלים',
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
            )],
            default_mode=dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
            ),
        ) for w in await self.get_wings(admissions=admissions)]

        views += [dict(
            type='department',
            key=f"D{d['key']}",
            name=d['name'],
            short_name=d['short_name'],
            department_id=d['key'],
            patients=d['patients'],
            patients_count=len(d['patients']),
            color=view_colors.get(f"D{d['key']}"),
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
            ), dict(
                key='department',
                name='תצוגת אגפים',
                short_name='אגפים',
            )],
            default_mode=dict(
                key='department',
                name='תצוגת אגפים',
                short_name='אגפים',
            ),
        ) for d in await self.get_departments(admissions=admissions)]

        views += [dict(
            type='custom',
            key=f"Vtrauma",
            name='מחלקת טראומה',
            short_name='טראומה',
            patients=[],
            patients_count=len([]),
            modes=[dict(
                key='trauma',
                name='תצוגה סיכומית',
                short_name='סיכומי',
            )],
            default_mode=dict(
                key='trauma',
                name='תצוגה סיכומית',
                short_name='סיכומי',
            ),
            # patients_count=len(await get_records()),
        )]

        return views

    async def get_departments(
            self,
            key: Optional[str] = None,
            admissions: Optional[List[Tuple[str, str, str]]] = None
    ) -> List[Dict]:
        department_names = {}
        department_short_names = {}
        department_indices = {}
        for department in (await self.application_dal.get_config('departments', []))['value']:
            department_names[department['key']] = department['name']
            department_short_names[department['key']] = department['short_name']
            department_indices[department['key']] = department['index']

        wing_indices = {}
        for wing in (await self.application_dal.get_config('wings', []))['value']:
            wing_indices.setdefault(wing['department'], {}).__setitem__(wing['key'], wing.get('index'))

        if not admissions:
            admissions = [admission async for admission in self.get_patient_admissions(
                {'admission.department_id': key} if key else {}
            )]

        return [dict(
            key=department,
            name=department_names.get(department, department),
            short_name=department_short_names.get(department, department),
            wing_ids=list(sorted(
                {w for o, d, w in admissions if d == department} | set(wing_indices.get(department, {})),
                key=lambda w: wing_indices.get(department, {}).get(w, 0), reverse=True
            )),
            patients=[dict(oid=o) for o, d, w in admissions if d == department],
        ) for department in ([key] if key else sorted(
            {d for o, d, w in admissions} | set(department_names),
            key=lambda d: department_indices.get(d, 0), reverse=True
        ))]

    async def get_wings(
            self,
            department: Optional[str] = None,
            key: Optional[str] = None,
            admissions: Optional[List[Tuple[str, str, str]]] = None,
    ) -> List[Dict]:
        wing_names = {}
        wing_layout = {}
        wing_indices = {}
        for wing in (await self.application_dal.get_config('wings', []))['value']:
            if department and wing['department'] != department:
                continue
            wing_names.setdefault(wing['department'], {}).__setitem__(wing['key'], wing['name'])
            if wing.get('beds') and wing.get('rows') and wing.get('columns'):
                wing_layout.setdefault(wing['department'], {}).__setitem__(wing['key'], {
                    'beds': wing['beds'],
                    'rows': wing['rows'],
                    'columns': wing['columns'],
                })
            wing_indices.setdefault(wing['department'], {}).__setitem__(wing['key'], wing.get('index', 0))
        if not admissions:
            admissions = [admission async for admission in self.get_patient_admissions(dict(
                **{'admission.department_id': department} if department else {},
                **{'admission.wing_id': key if key != 'wingless' else None} if key else {},
            ))]
        res = [dict(
            key=wing or 'wingless',
            department=d,
            name=wing_names.get(d, {}).get(wing, wing or 'ללא אגף'),
            details=dict(
                index=wing_indices.get(d, {}).get(wing, 0),
                layout=wing_layout.get(d, {}).get(wing, None),
            ),
            patients=(patients := [dict(oid=o) for o, dp, w in admissions if w == wing and dp == d]),
            patients_count=len(patients),
        ) for wing, d in ([(key, department)] if key and department else sorted(
            {(w, d) for o, d, w in admissions} | set((name, d) for d in wing_names for name in wing_names[d]),
            key=lambda w_d: wing_indices.get(w_d[1], {}).get(w_d[0], 0), reverse=True
        ))]
        return res

    async def get_bed(self, department: str, wing: str, bed: str) -> Optional[str]:
        async for oid, _ in self.get_patient_members({
            "admission.department_id": department, "admission.wing_id": wing, "admission.bed": bed
        }, members={'dummy'}):
            if oid:
                return oid

    async def get_patients(self, department: Optional[str], wing: Optional[str], bed: Optional[str],
                           oid: Optional[str], members: Set[str]):
        patient_members = {key: patient async for key, patient in self.get_patient_members(dict(
            **{'admission.department_id': department} if department else {},
            **{'admission.wing_id': wing if wing != 'wingless' else None} if wing else {},
            **{'admission.bed': bed} if bed else {},
            **{'_id': ObjectId(oid)} if oid else {},
        ), members=members)}
        return [dict(
            oid=o,
            notifications=[dict(key=key, **value) for key, value in patient.pop('notifications', {}).items()],
            watching=[dict(key=key, **value) for key, value in patient.pop('watching', {}).items()],
            **(dict(admission=dict(
                wing_id=(admission := patient.pop('admission')).pop('wing_id') or 'wingless',
                **admission
            )) if 'admission' in members else {}),
            **patient
        ) for o, patient in patient_members.items()]

    async def get_wing_filters(self, parent):
        patients = {oid: patient async for oid, patient in self.get_patient_entries({
            'admission.wing_id': parent['key'] if parent['key'] != 'wingless' else None,
            'admission.department_id': parent['department'],
        })}

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
            time_diff = (datetime.datetime.now(tz=pytz.UTC) - datetime.datetime.fromisoformat(
                patient.admission.arrival).astimezone(tz=pytz.UTC)).total_seconds() / 3600
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
        return dict(
            doctors=[
                        dict(
                            key=".".join(["physician", "ללא"]),
                            count=len(patients) - len(doctor_total),
                            title="ללא",
                            valid=False,
                            icon="doctor",
                        ),
                    ] + [
                        dict(
                            key=".".join(["physician", doctor.replace('.', '')]),
                            count=len(patients),
                            title=doctor.replace('.', ''),
                            valid=True,
                            icon="doctor",
                        )
                        for doctor, patients in doctors.items()
                    ],
            treatments=[
                           dict(
                               key=".".join(["treatment", "ללא"]),
                               count=len(patients) - len(treatment_total),
                               title="לא הוחלט",
                               valid=False,
                               icon="treatment",
                           ),
                       ] + [
                           dict(
                               key=".".join(["treatment", treatment.replace('.', '')]),
                               count=len(patients),
                               title=treatment.replace('.', ''),
                               valid=True,
                               icon="treatment",
                           )
                           for treatment, patients in treatments.items()
                       ],
            awaiting=[dict(
                key="awaiting",
                count=len(awaiting_total),
                title="ממתינים.ות",
                valid=True,
                icon="awaiting",
            )] + [dict(
                key=".".join(['awaiting', awaiting]),
                count=len(set(p for l in keys.values() for p, _ in l)),
                icon=awaiting,
                title=awaiting_name,
                valid=True,
                duration=average_date([d for l in keys.values() for _, d in l]),
                parent="awaiting"
            ) for (awaiting, awaiting_name), keys in awaitings.items()] + [dict(
                key=".".join(['awaiting', awaiting, key]),
                count=len(patients),
                title=key_name,
                icon=awaiting,
                valid=True,
                duration=average_date([d for _, d in patients]),
                parent=".".join(['awaiting', awaiting]),
            ) for (awaiting, awaiting_name), keys in awaitings.items()
                         for (key, key_name), patients in keys.items()] + [dict(
                key="not-awaiting",
                count=len(patients) - len(awaiting_total),
                title="ממתינים.ות להחלטה",
                icon="awaiting",
                valid=False,
            ), dict(
                key='waiting-intake',
                count=len(waiting_intake),
                title="אחות ממיינת",
                icon="awaiting",
                valid=False
            )
                     ],
            time_since_arrival=[dict(
                key=".".join(["time_since", time_since.replace('.', '')]),
                count=len(patients),
                title=f"ממתינים.ות {time_since} שעות",
                icon="awaiting",
                valid=True
            ) for time_since, patients in time_since_arrival.items()],
            mapping=[dict(key=k, values=v) for k, v in (
                    [
                        (".".join(["treatment", treatment]), patients) for
                        treatment, patients in treatments.items()
                    ] + [
                        (".".join(["treatment", "ללא"]),
                         list({oid for oid in patients} - treatment_total))
                    ] + [
                        (".".join(["physician", doctor]), patients) for
                        doctor, patients in doctors.items()
                    ] + [
                        (".".join(["physician", "ללא"]),
                         list({oid for oid in patients} - doctor_total))
                    ] + [
                        (".".join(['awaiting', awaiting, key]),
                         [p for p, _ in patients])
                        for (awaiting, awaiting_name), keys in awaitings.items()
                        for (key, key_name), patients in keys.items()
                    ] + [
                        (".".join(['awaiting', awaiting]),
                         list(set(
                             patient for patients in keys.values() for patient, _ in
                             patients)))
                        for (awaiting, awaiting_name), keys in awaitings.items()
                    ] + [
                        ("awaiting", list(awaiting_total)),
                        ("not-awaiting",
                         list({oid for oid in patients} - awaiting_total)),
                    ] + [
                        ("waiting-intake", waiting_intake)
                    ] + [
                        (".".join(["time_since", time_since]), patients)
                        for time_since, patients in time_since_arrival.items()
                    ]
            )]

        )

    async def get_patient_members(self, query, members) -> AsyncIterable[Tuple[str, Dict]]:
        async for patient in self.db.patients.find(query, {k: 1 for k in members}):
            yield str(patient.pop('_id')), patient

    async def get_patient_entries(self, query) -> AsyncIterable[Tuple[str, Patient]]:
        async for oid, patient in self.get_patient_members(query=query, members=[]):
            yield oid, Patient(**patient)

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
                            wing_id=MCI_INTAKE_MAPPING.get(existing_patient.admission.wing_id),
                        )
                    )

            with AtomicUpdate.set_connection(self):
                await Patient.atomic_update({"external_id": f'mci#{patient_id}'}, update=_update, create=_create)

    async def update_patient(self, patient_query: dict, path: List[str], value: Any, type_: str | bool):
        if type_:
            value = {
                'Severity': Severity.parse,
                'WatchKey': WatchKey.parse,
                'MCIBooleanValue': MCIBooleanValue.parse,
                'MCIStringValue': MCIStringValue.parse,
                'MCIListItemValue': MCIListItemValue.parse,
                'Admission': Admission.parse,
                'MCIList': lambda v: [MCIListItemValue(**item) for item in v],
            }[type_](value)

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

    async def insert_patient(self, patient: Patient) -> str:
        async def _create() -> Patient:
            return Patient(
                version=patient.version,
                external_id=patient.external_id,
                info=patient.info,
                admission=patient.admission,
                source_identity=patient.source_identity,
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
            oid = await Patient.atomic_update({"external_id": patient.external_id}, create=_create)
        return oid

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

    async def merge_mci_patient(self, anonymous_id, patient_id):
        anon_oid, anon_patient = await  self.get_patient({'external_id': anonymous_id})

        async def update_patient(patient) -> None:
            patient.mci = anon_patient.mci
            patient.source_identity = anon_oid

        async def update_anonymous(anonymous) -> None:
            anonymous.source_identity = 'merged'

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update=update_patient)
        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": anonymous_id}, update=update_anonymous)

    async def unmerge_mci_patient(self, patient_id):
        old_patient = await  self.get_patient({'external_id': patient_id})
        anonymous_patient = await self.get_patient({'_id': ObjectId(old_patient.source_identity)})

        async def update_patient(patient) -> None:
            patient.mci = {}
            patient.source_identity = None

        async def update_anonymous(patient) -> None:
            patient.source_identity = 'manually'
            patient.mci = old_patient.mci

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": anonymous_patient.external_id}, update=update_anonymous)
        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"external_id": patient_id}, update=update_patient)

    async def update_mci(self, results: list, id_: str):
        async def update(patient) -> None:
            patient.mci_results = results

        with AtomicUpdate.set_connection(self):
            await Patient.atomic_update({"info.id_": id_, "external_id": {"$regex": "^mci"}}, update)
