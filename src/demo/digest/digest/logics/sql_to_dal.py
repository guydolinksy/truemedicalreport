import contextlib
from enum import Enum

import logbook
import pytz
import requests
from requests import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sentry_sdk import capture_message
from common.data_models.admission import Admission
from common.data_models.esi_score import ESIScore
from common.data_models.image import ImagingStatus, Image, ImagingTypes
from common.data_models.labs import Laboratory, LabStatus, CATEGORIES_IN_HEBREW
from common.data_models.measures import Measure, MeasureType
from common.data_models.notification import NotificationLevel
from common.data_models.patient import Intake, ExternalPatient, Person
from common.data_models.referrals import Referral
from common.data_models.treatment import Treatment
from .. import config
from ..utils import sql_statements, utils

logger = logbook.Logger(__name__)

DEMO_IMAGING_STATUS = {
    103: ImagingStatus.performed,  # הסתיימה
    106: ImagingStatus.ordered,  # שובץ
    108: ImagingStatus.performed,  # לא פוענח
    109: ImagingStatus.performed,  # לא פוענח
    111: ImagingStatus.analyzed,  # פוענח
    112: ImagingStatus.analyzed,  # הוקלד
    114: ImagingStatus.verified,  # אושרר
    119: ImagingStatus.ordered,  # הפנייה חדשה
    120: ImagingStatus.cancelled,  # בוטל ע"י טכנאי
    122: ImagingStatus.cancelled,  # הפנייה נדחתה
    125: ImagingStatus.ordered,  # הפנייה אושרה
    127: ImagingStatus.analyzed,  # הפנייה לאישור
}

DEMO_IMAGING_LEVEL = {
    0: NotificationLevel.normal,
    1: NotificationLevel.panic,
}
DEMO_XRAY_CODES = [2251, 2259, 2937, 3009, 3103, 3104, 3113, 3114, 3115, 3116, 3117, 3121, 3124, 3131, 3132, 3134, 3140,
                   3142, 3144, 3159, 3163, 3166, 3171, 3173, 3180, 3184, 3185, 3195, 3201, 3202, 3217, 3223, 3230, 3529,
                   3580, 3604, 3620, 3650, 3658, 3661, 3678, 3695, 3735, 3821, 3826, 3895, 3897, 3898, 3899, 3923, 3969,
                   4040, 4297, 4364, 4365, 4366, 4367, 4430, 4569, 4660]
DEMO_CT_CODES = [1794, 2944, 3493, 3579, 3582, 3583, 3585, 3586, 3587, 3588, 3594, 3605, 3608, 3610, 3611, 3612, 3613,
                 3614, 3615, 3616, 3617, 3618, 3619, 3621, 3622, 3624, 3625, 3626, 3627, 3628, 3629, 3630, 3631, 3632,
                 3633, 3634, 3635, 3636, 3637, 3638, 3639, 3640, 3641, 3642, 3643, 3644, 3645, 3646, 3647, 3648, 3649,
                 3651, 3652, 3653, 3654, 3655, 3657, 3659, 3662, 3663, 3664, 3665, 3666, 3667, 3668, 3669, 3671, 3672,
                 3673, 3674, 3675, 3681, 3683, 3684, 3685, 3686, 3687, 3690, 3693, 3694, 3696, 3705, 3707, 3709, 3710,
                 3711, 3712, 3713, 3714, 3715, 3716, 3717, 3720, 3721, 3722, 3723, 3724, 3725, 3731, 3737, 3740, 3749,
                 3751, 3752, 3753, 3757, 3767, 3768, 3769, 3776, 3779, 3782, 3783, 3791, 3800, 3814, 3819, 3822, 3823,
                 3824, 3846, 3850, 3851, 3853, 3857, 3860, 3868, 3869, 3879, 3880, 3881, 3882, 3883, 3887, 3890, 3891,
                 3894, 3901, 3905, 3907, 3910, 3921, 3924, 3934, 3935, 3937, 3958, 3961, 3962, 3963, 3972, 3973, 3975,
                 3980, 3982, 3984, 3987, 3988, 3995, 3999, 4010, 4011, 4013, 4014, 4015, 4019, 4021, 4022, 4025, 4027,
                 4036, 4039, 4055, 4064, 4094, 4095, 4097, 4128, 4129, 4130, 4132, 4137, 4150, 4174, 4175, 4177, 4181,
                 4182, 4185, 4188, 4223, 4225, 4226, 4230, 4232, 4233, 4270, 4290, 4291, 4293, 4316, 4318, 4333, 4341,
                 4344, 4355, 4356, 4370, 4387, 4400, 4410, 4414, 4429, 4465, 4467, 4477, 4484, 4510, 4535, 4547, 4556,
                 4560, 4565, 4568, 4570, 4574, 4579, 4581, 4583, 4585, 4586, 4606, 4611, 4612, 4622, 4624, 4626, 4629,
                 4637, 4638, 4639, 4643, 4644, 4645, 4647, 4650, 4651, 4652, 4653, 4654, 4658, 4664, 4701, 4773, 4785,
                 4917, 4918, 5026, 5027]
DEMO_MRI_CODES = [2947, 2948, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2958, 2959, 2960, 2961, 2962, 2963,
                  2964, 2965, 2966, 2967, 2968, 2969, 2970, 2971, 2972, 2973, 2974, 2976, 2977, 2978, 2979, 2980, 2981,
                  2982, 2983, 2984, 2985, 2986, 2987, 2988, 2989, 2990, 2991, 2992, 2993, 2994, 2995, 2996, 2997, 2998,
                  2999, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3010, 3011, 3024, 3025, 3028, 3029, 3030,
                  3038, 3039, 3040, 3042, 3043, 3050, 3051, 3056, 3057, 3059, 3064, 3067, 3069, 3071, 3072, 3075, 3078,
                  3080, 3083, 3085, 3086, 3098, 3122, 3155, 3157, 3162, 3172, 3174, 3175, 3177, 3187, 3189, 3190, 3194,
                  3208, 3209, 3218, 3221, 3481, 3482, 3494, 3508, 3515, 3526, 3527, 3530, 3531, 3547, 3574, 3598, 3606,
                  3623, 3656, 3660, 3689, 3718, 3775, 3827, 3830, 3834, 3844, 3867, 3903, 3915, 3919, 3948, 3960, 3966,
                  3970, 3990, 3992, 3993, 3996, 3997, 4012, 4017, 4028, 4050, 4051, 4057, 4147, 4153, 4172, 4184, 4219,
                  4220, 4224, 4271, 4332, 4368, 4378, 4391, 4392, 4399, 4401, 4422, 4424, 4428, 4432, 4478, 4529, 4544,
                  4545, 4553, 4559, 4562, 4571, 4577, 4578, 4582, 4587, 4589, 4591, 4595, 4597, 4598, 4599, 4602, 4604,
                  4609, 4615, 4630, 4641, 4698, 4745, 4800, 4819, 4822, 4847, 4864, 4868, 4892, 5040, 5042, 5046, 5047,
                  5048, 5049, 5050, 5052, 5055]
DEMO_MEASUREMENT_CODES = {
    1: MeasureType.temperature,
    3: MeasureType.pulse,
    4: MeasureType.weight,
    9: MeasureType.urine_output,
    12: MeasureType.breaths,
    13: MeasureType.saturation,
    23: MeasureType.systolic,
    24: MeasureType.diastolic,
    61: MeasureType.pain,
    542: MeasureType.enriched_saturation,
}


class Departments(Enum):
    er = '1184000'


class FreeTextCodes(Enum):
    DOCTOR_VISIT = 1
    DOCTOR_SUMMARY = 889
    NURSE_SUMMARY = 901


class SqlToDal(object):
    def __init__(self, db_connection=None, dal_url=None):
        self.dal_url = dal_url or config.dal_url

        db_connection = db_connection or config.db_connection
        self._engine = create_engine(db_connection)

    @contextlib.contextmanager
    def session(self):
        with Session(self._engine) as session:
            yield session

    def update_admissions(self, department: Departments):
        try:
            logger.debug('Getting admissions for `{}`...', department.name)

            patients = []
            with self.session() as session:
                for row in session.execute(sql_statements.query_patient_admission.format(unit=department.value)):
                    patients.append(ExternalPatient(
                        external_id=row["MedicalRecord"],
                        info=Person(
                            id_=row["MedicalRecord"],
                            name=row["FullName"],
                            gender='male' if row["Gender"] == 'זכר' else 'female',
                            birthdate=utils.datetime_utc_serializer(row["BirthDate"]),
                            age=utils.calculate_patient_age(row["BirthDate"]),
                        ),
                        esi=ESIScore(
                            value=row["ESI"],
                            at=utils.datetime_utc_serializer(row["AdmissionDate"]),
                        ),
                        admission=Admission(
                            department=department.name,
                            wing=row["RoomName"],
                            bed=row["BedName"],
                            arrival=utils.datetime_utc_serializer(row["AdmissionDate"]),
                        ),
                        intake=Intake(
                            complaint=row["MainCause"],
                        ),
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/admissions',
                                json={'admissions': patients})
            res.raise_for_status()

            return {'admissions': patients}
        except HTTPError:
            logger.exception('Could not run admissions handler.')

    def update_measurements(self, department: Departments):
        try:
            logger.debug('Getting measurements for `{}`...', department.name)

            measures = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_measurements.format(
                        unit=department.value, codes='{}'.format(','.join(map(str, DEMO_MEASUREMENT_CODES)))
                )):
                    measures.setdefault(row['MedicalRecord'], []).append(Measure(
                        value=row['Result'],
                        minimum=row['MinValue'],
                        maximum=row['MaxValue'],
                        at=utils.datetime_utc_serializer(row['At']),
                        type=DEMO_MEASUREMENT_CODES.get(row['Code'], MeasureType.other),
                        external_id=row['MeasureID'],
                    ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/measurements',
                                json={'measurements': measures})
            res.raise_for_status()
            return {'measurements': measures}
        except HTTPError:
            logger.exception('Could not run measurements handler.')

    def update_imaging(self, department: Departments):
        try:
            logger.debug('Getting imaging for `{}`...', department.name)
            imaging = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_images.format(unit=department.value)):
                    imaging.setdefault(row['MedicalRecord'], []).append(Image(
                        external_id=row['OrderNumber'],
                        patient_id=row['MedicalRecord'],
                        ordered_at=utils.datetime_utc_serializer(row['OrderDate']),
                        code=row["Code"],
                        imaging_type=self._get_imaging_type_by_code(row["Code"]),
                        title=row['TestName'],
                        status=DEMO_IMAGING_STATUS.get(row['OrderStatus'], ImagingStatus.unknown),
                        interpretation=row['Result'],
                        level=DEMO_IMAGING_LEVEL.get(row['Panic'], NotificationLevel.normal),
                        link='https://localhost/',
                    ).dict(exclude_unset=True))
                res = requests.post(f'{self.dal_url}/departments/{department.name}/imaging', json={'images': imaging})
                res.raise_for_status()
                return {'images': imaging}
        except HTTPError:
            logger.exception('Could not run imaging handler.')

    @staticmethod
    def _get_imaging_type_by_code(code: str) -> ImagingTypes:
        if code in DEMO_XRAY_CODES:
            return ImagingTypes.xray
        elif code in DEMO_CT_CODES:
            return ImagingTypes.ct
        elif code in DEMO_MRI_CODES:
            return ImagingTypes.mri
        return ImagingTypes.unknown

    def update_labs(self, department: Departments):
        try:
            logger.debug('Getting labs for `{}`...', department.name)
            labs = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_labs.format(unit=department.value)):
                    try:
                        labs.setdefault(row['MedicalRecord'], []).append(self._update_lab(row).dict(
                            exclude_unset=True))
                    except KeyError as e:
                        msg = f"Lab from category '{row['Category'].strip()}' isn't exists in internal mapping " \
                              f"for medical record {row['MedicalRecord']}"
                        capture_message(msg, level="warning")
                        logger.error(msg)

            res = requests.post(f'{self.dal_url}/departments/{department.name}/labs',
                                json={"labs": labs})
            res.raise_for_status()
            return {"labs": labs}
        except HTTPError as e:
            logger.exception(f'Could not run labs handler. {e}')

    @staticmethod
    def _update_lab(row) -> Laboratory:
        if row["ResultTime"] is None:
            status = LabStatus.ordered
            result_at = None
        else:
            status = LabStatus.analyzed
            result_at = utils.datetime_utc_serializer(row["ResultTime"])

        ordered_at = utils.datetime_utc_serializer(row["OrderDate"])
        category = row["Category"].strip()
        return Laboratory(
            patient_id=row['MedicalRecord'],
            external_id=f'{row["MedicalRecord"]}#{ordered_at}#{row["TestCode"]}',
            ordered_at=ordered_at,
            result_at=result_at,
            test_type_id=row["TestCode"],
            test_type_name=row["TestName"],
            category_id=category,
            category_name=CATEGORIES_IN_HEBREW[category],
            range=row["Range"],
            panic=row["Panic"],
            result=row["Result"],
            status=status
        )

    def update_doctor_intake(self, department: Departments):
        try:
            logger.debug('Getting doctor intake for `{}`...', department.name)
            infos = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_doctor_intake.format(unit=department.value)):
                    intake = infos.setdefault(row['MedicalRecord'], Intake())
                    intake.doctor_seen_time = utils.datetime_utc_serializer(row['DocumentingTime']) \
                        if row['DocumentingTime'] else None
            res = requests.post(
                f'{self.dal_url}/departments/{department.name}/intake',
                json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
            )
            res.raise_for_status()
            return {'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        except HTTPError:
            logger.exception('Could not run doctor intake handler.')

    def update_nurse_intake(self, department: Departments):
        try:
            logger.debug('Getting nurse intake for `{}`...', department.name)
            infos = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_nurse_intake.format(unit=department.value)):
                    intake = infos.setdefault(row['MedicalRecord'], Intake())
                    intake.nurse_description = row['MedicalText']
                    intake.nurse_seen_time = utils.datetime_utc_serializer(row['DocumentingTime']) \
                        if row['DocumentingTime'] else None
            res = requests.post(
                f'{self.dal_url}/departments/{department.name}/intake',
                json={'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
            )
            res.raise_for_status()
            return {'intakes': {record: infos[record].dict(exclude_unset=True) for record in infos}}
        except HTTPError:
            logger.exception('Could not run nurse intake handler.')

    def update_referrals(self, department: Departments):
        try:
            logger.debug('Getting referrals for `{}`...', department.name)
            referrals = {}
            treatments = {}
            with self.session() as session:
                for row in session.execute(sql_statements.query_referrals.format(unit=department.value)):
                    if row['MedicalLicense']:
                        treatments.setdefault(row['MedicalRecord'], Treatment()).doctors.append(
                            f'{row["Title"]} {row["FirstName"]} {row["LastName"]}'
                        )
                    else:
                        referrals.setdefault(row['MedicalRecord'], []).append(Referral(
                            external_id=row['ReferralId'],
                            patient_id=row['MedicalRecord'],
                            at=utils.datetime_utc_serializer(row['ReferralDate']) if row['ReferralDate'] else None,
                            to=row['LastName'],
                        ).dict(exclude_unset=True))
            res = requests.post(f'{self.dal_url}/departments/{department.name}/treatments',
                                json={record: treatments[record].dict(exclude_unset=True) for record in treatments})
            res.raise_for_status()
            res = requests.post(f'{self.dal_url}/departments/{department.name}/referrals',
                                json={'referrals': referrals})
            res.raise_for_status()
            return {'treatments': {record: treatments[record].dict(exclude_unset=True) for record in treatments},
                    'referrals': referrals}
        except HTTPError:
            logger.exception('Could not run referrals handler.')

    def update_destination(self, department: Departments):
        treatments = {}
        try:
            logger.debug('Getting treatments for `{}`...', department.name)
            with self.session() as session:
                for row in session.execute(sql_statements.query_treatment.format(unit=department.value)):
                    treatments[row["MedicalRecord"]] = \
                        Treatment(destination=row["UnitName"] or row["Decision"]).dict(exclude_unset=True)
            res = requests.post(f'{self.dal_url}/departments/{department.name}/treatments', json=treatments)
            res.raise_for_status()
            return {'treatments': treatments}
        except IndexError as e:
            logger.exception("No Data Fetched From SQL", e)
        except HTTPError:
            logger.exception('Could not update treatments')

    def update_medicines(self, department: Departments):
        medicine = {}
        try:
            return {'medicines': medicine}
        except IndexError as e:
            logger.exception("No Data Fetched From SQL", e)
        except HTTPError:
            logger.exception('Could not update treatments')
