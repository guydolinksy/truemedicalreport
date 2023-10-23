import requests

from digest import config

CHECKBOX = 'checkbox'
COLLAPSE = 'collapse'
DEFAULT = [
    dict(
        key='details',
        name='פרטים',
        options=[
            dict(
                key='soldier',
                name='חייל',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='civilian',
                name='אזרח',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='by_air',
                name='מסוק',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='by_car',
                name='אמבולנס',
                default=False,
                type=CHECKBOX,
            ),
        ],
    ),
    dict(
        key='diagnosis',
        name='מנגנון פציעה',
        options=[
            dict(
                key='gunshot',
                name='פצע ירי',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='head_trauma',
                name='פגיעת ראש',
                default=False,
                type=CHECKBOX,
            )
            ,
            dict(
                key='stabbing',
                name='פצע דקירה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='burns',
                name='כוויות',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='blast',
                name='פגיעת הדף',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='amputation',
                name='קטיעת גפה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='crush',
                name='פגיעת מעיכה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='shrapnel',
                name='פגיעה חודרת מרסיסים',
                default=False,
                type=CHECKBOX,
            ),
        ],
    ),
    dict(
        key='pre_hospital_treatment',
        name='טיפול בשטח',
        options=[
            dict(
                key='pre_hospital_blood_unit',
                name='מנת דם',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='pre_hospital_tourniquet',
                name='חוסם עורקים',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='pre_hospital_intubation',
                name='הנשמה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='pre_hospital_chest_drain',
                name='נקז חזה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='needle',
                name='Needle',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='b_i_g',
                name='B.I.G',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='coniotomy',
                name='Coniotomy',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='plasma_transfusion',
                name='מנות פלזמה',
                default=False,
                type=COLLAPSE,
                children=[
                    dict(
                        key='plasma_unit_1',
                        name='1',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_2',
                        name='2',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_3',
                        name='3',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_4',
                        name='4',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_5',
                        name='5',
                        default=False,
                        type=CHECKBOX,
                    ),
                ],
            ),
        ],
    ),
    dict(
        key='hospital_treatment',
        name='טיפול בבית חולים',
        options=[

            dict(
                key='blood_type',
                name='דם לסוג והצלבה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='high_flow',
                name='High Flow',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='infusion',
                name='עירוי',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='blood_transfusion',
                name='מנות דם',
                default=False,
                type=COLLAPSE,
                children=[
                    dict(
                        key='blood_unit_1',
                        name='1',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='blood_unit_2',
                        name='2',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='blood_unit_3',
                        name='3',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='blood_unit_4',
                        name='4',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='blood_unit_5',
                        name='5',
                        default=False,
                        type=CHECKBOX,
                    ),
                ],
            ),
            dict(
                key='plasma_transfusion',
                name='מנות פלזמה',
                default=False,
                type=COLLAPSE,
                children=[
                    dict(
                        key='plasma_unit_1',
                        name='1',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_2',
                        name='2',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_3',
                        name='3',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_4',
                        name='4',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='plasma_unit_5',
                        name='5',
                        default=False,
                        type=CHECKBOX,
                    ),
                ],
            ),
            dict(
                key='tourniquet_removal',
                name='הסרת חוסם',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='chest_drain',
                name='נקז חזה',
                default=False,
                type=COLLAPSE,
                children=[
                    dict(
                        key='left_chest_drain',
                        name='שמאל',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='right_chest_drain',
                        name='ימין',
                        default=False,
                        type=CHECKBOX,
                    ),
                ],
            ),
            dict(
                key='intubation',
                name='הנשמה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='urinary_catheter',
                name='קטטר',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='ng_tube',
                name='זונדה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='immobilization',
                name='קיבועים',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='medications',
                name='תרופות',
                default=False,
                type=COLLAPSE,
                children=[
                    dict(
                        key='iv_fentanyl',
                        name='IV FENTANYL',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='iv_morphine',
                        name='IV MORPHINE',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='iv_ketamin',
                        name='IV KETAMIN',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='iv_cefamezin',
                        name='IV CEFAMEZIN',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='im_toxoid',
                        name='IM TOXOID',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='iv_kepra',
                        name='IV KEPRA',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='hexakapron',
                        name='HEXAKAPRON',
                        default=False,
                        type=CHECKBOX,
                    )
                ]
            ),
        ],
    ), dict(
        key='imaging',
        name='הדמיה',
        options=[
            dict(
                key='chest_xray',
                name='צילום חזה',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='fast',
                name='FAST',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='ct',
                name='CT',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='angiogram',
                name='Angio',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='mri',
                name='MRI',
                default=False,
                type=CHECKBOX,
            ),
        ],
    ), dict(
        key='destination',
        name='יעד',
        options=[
            dict(
                key='er_imaging',
                name='הדמייה במלר"ד',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='operating_room',
                name='חדר ניתוח',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='general_imaging',
                name='הדמייה באתר בירורים',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='intensive_care',
                name='טיפול נמרץ כללי',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='cardiac_intensive_care',
                name='טיפול נמרץ לב',
                default=False,
                type=CHECKBOX,
            ),
            dict(
                key='hospitalization',
                name='אשפוז',
                default=False,
                type=COLLAPSE,
                children=[
                    dict(
                        key='trauma_unit',
                        name='יחידת הטראומה',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='surgical_b',
                        name='כירוגיה ב',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='surgical_c',
                        name='כירוגיה ג',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='neurosurgical',
                        name='נוירוכירוגיה',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='orthopedics_a',
                        name='אורתופדיה א',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='orthopedics_b',
                        name='אורתופדיה ב',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='hand_palm',
                        name='כף יד',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='mouth_and_jaw',
                        name='פה ולסת',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='ent',
                        name='אף אוזן גרון',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='urology',
                        name='אורולוגיה',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='chest_and_blood_vessels',
                        name='חזה וכלי דם',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='pediatric',
                        name='ילדים',
                        default=False,
                        type=CHECKBOX,
                    ), dict(
                        key='pediatric_icu',
                        name='טיפול נמרץ ילדים',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_a',
                        name='פנימית א',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_b',
                        name='פנימית ב',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_c',
                        name='פנימית ג',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_d',
                        name='פנימית ד',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_e',
                        name='פנימית ה',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_f',
                        name='פנימית ו',
                        default=False,
                        type=CHECKBOX,
                    ),
                    dict(
                        key='internal_medicine_h',
                        name='פנימית ט',
                        default=False,
                        type=CHECKBOX,
                    ),
                ],
            ),
        ],
    )]


async def init_mci_form():
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'mci_form',
        'version': 1,
        'value': DEFAULT,
    }).raise_for_status()
