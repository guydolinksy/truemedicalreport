import requests

from common.mci import MCI_DEPARTMENT, MCIIntakeWing, MCI_COLORS, MCI_NAMES
from digest import config

DEFAULT_MCI_PANEL_FORMAT = dict(
    components=[
        dict(
            key='info',
            type='PatientInfo',
            name="מידע",
            config=dict(
                customStyle=dict(
                    flexBasis='100%',
                ),
            ),
        ),
        dict(
            key='header',
            type='MCIHeader',
            name="פרטים מזהים",
            config=dict(
                key='header',
                customStyle=dict(
                    flexBasis='100%',
                ),
                sections=[
                    dict(
                        key='occupation',
                        options=[
                            dict(
                                key="soldier",
                                name="חייל",
                            ), dict(
                                key="civilian",
                                name="אזרח",
                            ),
                        ],
                    ),
                    dict(
                        key='transport',
                        options=[
                            dict(
                                key="by-air",
                                name="מסוק",
                            ), dict(
                                key="by-land",
                                name="אמבולנס",
                            ),
                        ],
                    ),
                ],
            ),
        ),
        dict(
            key='diagnosis',
            type='MCISection',
            name='מנגנון פציעה',
            config=dict(
                key='diagnosis',
                name='מנגנון פציעה',
                customStyle=dict(
                    flex=1
                ),
                options=[dict(
                    key="gunshot",
                    name="פצע ירי",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="stab_wound",
                    name="פצע דקירה",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="burn",
                    name="כוויה",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="blast",
                    name="פגיעת הדף",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="amputation",
                    name="קטיעה",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="crush",
                    name="פגיעת מעיכה",
                    short_name='פ. מעיכה',
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="shrapnel",
                    name="פגיעה חודרת מרסיס",
                    short_name='פ. רסיס',
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                )]
            ),
        ),
        dict(
            key='pre_hospital_treatment',
            type='MCISection',
            name='טיפול בשטח',
            config=dict(
                key='pre_hospital_treatment',
                name='טיפול בשטח',
                customStyle=dict(
                    flex=1
                ),
                options=[dict(
                    key="blood",
                    name="מנת דם",
                ), dict(
                    key="intubation",
                    name="הנשמה",
                ), dict(
                    key="chest_drain_left",
                    name="נקז חזה שמאל",
                ), dict(
                    key="chest_drain_right",
                    name="נקז חזה ימין",
                ), dict(
                    key="needle",
                    name="needle",
                ), dict(
                    key="b.i.g",
                    name="b.i.g",
                ), dict(
                    key="b.i.g",
                    name="b.i.g",
                ), dict(
                    key="tourniquet",
                    name="חסם עורקים",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="drug",
                    name="תרופה",
                    short_name="",
                    customizer=dict(
                        key='drugs',
                        name='סוג התרופה',
                        type='drugs',
                        options=[
                            dict(name='אדרנלין', dosage_amount=0.1, dosage_unit='mg', maximum=2),
                            dict(name='אקטיק', dosage_amount=1, dosage_unit='unit', maximum=1),
                            dict(name='פנטניל IV', dosage_amount=50, dosage_unit='um', maximum=100),
                            dict(name='מורפיום IV', dosage_amount=3, dosage_unit='mg', maximum=9),
                            dict(name='קטמין', dosage_amount=30, dosage_unit='mg', maximum=300),
                            dict(name='צפמזין', dosage_amount=2, dosage_unit='g', maximum=2),
                            dict(name='טוקסואיד IM', dosage_amount=0.5, dosage_unit='mg', maximum=1),
                            dict(name='קפרה', dosage_amount=1000, dosage_unit='mg', maximum=2000),
                            dict(name='הקסקפרון', dosage_amount=1000, dosage_unit='mg', maximum=2000),
                        ],
                    )
                )]
            ),
        ),
        dict(
            key='hospital_treatment',
            type='MCISection',
            name='טיפול בבית החולים',
            config=dict(
                key='hospital_treatment',
                name='טיפול בבית החולים',
                customStyle=dict(
                    flex=1
                ),
                options=[dict(
                    key="blood_type",
                    name="דם לסוג",
                ), dict(
                    key="high_flow",
                    name="High Flow",
                ), dict(
                    key="blood",
                    name="מנת דם",
                ), dict(
                    key="plasma",
                    name="פלזמה",
                ), dict(
                    key="platelets",
                    name="טסיות",
                ), dict(
                    key="tetanus",
                    name="טטנוס",
                ), dict(
                    key="tourniquet_removal",
                    name="הסרת חסם עורקים",
                    short_name='הסרת ח.ע.',
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="intubation",
                    name="הנשמה",
                ), dict(
                    key="chest_drain_left",
                    name="נקז חזה שמאל",
                ), dict(
                    key="chest_drain_right",
                    name="נקז חזה ימין",
                ), dict(
                    key="catheter",
                    name="קטטר",
                ), dict(
                    key="ng_tube",
                    name="זונדה",
                ), dict(
                    key="immobilization",
                    name="קיבוע",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location',
                    )
                ), dict(
                    key="drug",
                    name="תרופה",
                    short_name="",
                    customizer=dict(
                        key='drugs',
                        name='סוג התרופה',
                        type='drugs',
                        options=[
                            dict(name='אדרנלין', dosage_amount=0.1, dosage_unit='mg', maximum=2),
                            dict(name='אקטיק', dosage_amount=1, dosage_unit='unit', maximum=1),
                            dict(name='פנטניל IV', dosage_amount=50, dosage_unit='um', maximum=100),
                            dict(name='מורפיום IV', dosage_amount=3, dosage_unit='mg', maximum=9),
                            dict(name='קטמין', dosage_amount=30, dosage_unit='mg', maximum=300),
                            dict(name='צפמזין', dosage_amount=2, dosage_unit='g', maximum=2),
                            dict(name='טוקסואיד IM', dosage_amount=0.5, dosage_unit='mg', maximum=1),
                            dict(name='קפרה', dosage_amount=1000, dosage_unit='mg', maximum=2000),
                            dict(name='הקסקפרון', dosage_amount=1000, dosage_unit='mg', maximum=2000),
                        ],
                    )
                )]
            ),
        ),
        dict(
            key='imaging',
            type='MCISection',
            name='הדמיות וניתוחים',
            config=dict(
                key='imaging',
                name='הדמיות וניתוחים',
                customStyle=dict(
                    flex=1
                ),
                options=[dict(
                    key="surgical-operation",
                    name="מיועד לניתוח",
                ), dict(
                    key="mri",
                    name="MRI",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location'
                    )
                ), dict(
                    key="ct",
                    name="CT",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location'
                    )
                ), dict(
                    key="ct_angio",
                    name="CT Angio",
                    customizer=dict(
                        key='location',
                        name='מיקום',
                        type='location'
                    )
                ), dict(
                    key="cxr",
                    name="צילום חזה",
                ), dict(
                    key="fast",
                    name="FAST",
                ), dict(
                    key="echo",
                    name="אקו לב",
                )]
            ),
        ),
        dict(
            key='full_measures',
            type='FullMeasures',
            name="מדדים",
            config=dict(),
        ),
    ]
)
DEFAULT_PANEL_FORMAT = dict(
    components=[
        dict(
            key='info',
            type='PatientInfo',
            name="מידע",
            config=dict(
                customStyle=dict(
                    flexBasis='100%',
                ),
            ),
        ),
        dict(
            key='notes',
            type='Notes',
            name="הערות",
            config=dict(
                customStyle=dict(
                    flexBasis='100%',
                ),
            ),
        ),
        dict(
            key='basic_info',
            type='BasicInfo',
            name="מידע בסיסי",
            config=dict(),
        ),
        dict(key="medications",
             type="Medications",
             name="תרופות",
             config=dict()
             ),
        dict(
            key='full_measures',
            type='FullMeasures',
            name="מדדים",
            config=dict(),
        ),
        dict(
            key='notifications',
            type='Notifications',
            name="עדכונים",
            config=dict(),
        ),
        dict(
            key='labs',
            type='Labs',
            name="מעבדות",
            config=dict(),
        ),
        dict(
            key='labs',
            type='Cultures',
            name="מעבדות",
            config=dict(),
        ),
        dict(
            key='imaging',
            type='Imaging',
            name="הדמיות",
            config=dict(),
        ),
        dict(
            key='referrals',
            type='Referrals',
            name="הפניות",
            config=dict(),
        ),
        dict(
            key='medical_summary',
            type='MedicalSummary',
            name="סיכום רפואי",
            config=dict(),
        ),
        dict(
            key='ecg',
            type='ECGs',
            name="ECG",
            config=dict(),
        ),
        dict(
            key='era',
            type='PanelPlugin',
            name="ERA AI",
            config=dict(
                title='ERA AI',  # TODO: get from chart
                url='https://era.arc-prod.sheba.gov.il/widget/token?next=/widget/prediction/{info[id_]}&token={token}',
                api_version='v1'
            ),
        ),
    ]
)
NEW_MCI_VIEW = {
   "components": [
       {"key": "mci", "type": "MCI", "config": {
           "john_doe_name": "אלמוני/ת",
           "identification": [{"key": "id", "value": "ת.ז"}, {"key": "bracelet", "value": "מס' ידון"}],
           "age_groups": {"values": [{"key": "adult", "value": "בוגר"}, {"key": "child", "value": "ילד"}, {"key": "infant", "value": "תינוק"}], "default_value": "adult"},
           "tags": [
               {"key": "unconscious", "value": "חסר הכרה"},
               {"key": "shell_shock", "value": "תגובת קרב"},
               {"key": "smoke_inhalation", "value": "שאיפת עשן"},
               {"key": "crushing", "value": "מעיכה"},
               {"key": "blast", "value": "הדף"},
               {"key": "gunshot", "value": "ירי"},
               {"key": "kinematics", "value": "קינמטיקה"}
           ],
           "table": {"empty_text": "טרם נרשמו טיפולים"},
           "vitals": {"empty_text": "טרם נלקחו מדדים", "values": [
               {"key": "blood_pressure", "title": "B.P.", "value": "לחץ דם", "empty_text": "None"},
               {"key": "pulse", "title": "Pulse", "value": "דופק", "empty_text": "None"},
               {"key": "saturation", "title": "Saturation", "value": "סטורציה", "empty_text": "None"},
               {"key": "temperature", "title": "Temperature", "value": "חום", "empty_text": "None"},
           ]},
           "field_intake": {
               "identification": [{"key": "iron", "value": "מס' ברזל:"}],
               "toggles": [
                   {"key": "gender", "name": "מין", "values": [
                       {"key": "male", "name": "זכר"},
                       {"key": "female", "name": "נקבה"},
                   ], "default_value": "male"},
                   {"key": "age_group", "name": "גיל", "values": [
                       {"key": "adult", "name": "בוגר"},
                       {"key": "child", "name": "ילד"},
                       {"key": "infant", "name": "תינוק"},
                   ], "default_value": "adult"},
                   {"key": "occupation", "name": "חייל", "values": [
                       {"key": "civilian", "name": "אזרח"},
                       {"key": "soldier", "name": "חייל"},
                   ], "default_value": "civilian"},
                   {"key": "transport", "name": "הגעה", "values": [
                       {"key": "ambulance", "icon": "ambulance"},
                       {"key": "helicopter", "icon": "helicopter"},
                       {"key": "other", "name": "אחר"},
                   ], "default_value": "ambulance"},
               ],
               "diagnosis": {
                   "key": "pre_hospital_diagnosis",
                   "title": "מנגנון פציעה",
                   "values": [
                       {"key": "smoke_inhalation", "name": "שאיפת עשן"},
                       {"key": "unconventional", "name": 'אב"כ'},
                       {"key": "unconscious", "name": "חוסר הכרה"},
                   ],
               },
               "procedures": {
                   "title": "פרוצדורות בשטח",
                   "values": [
                       {"key": "intubation", "value": "אינטובציה"},
                       {"key": "troker", "value": "טרוקר"},
                       {"key": "coniotomia", "value": "קוניוטומיה"},
                       {"key": "zonda", "value": "זונדה"},
                       {"key": "tracheotomy", "value": "טרכוטומיה"},
                       {"key": "poly", "value": "פולי"},
                       {"key": "na", "value": "NA"},
                       {"key": "big", "value": "B.I.G"},
                   ]
               },
               "arteries": {
                   "title": "חוסם עורקים",
                   "values": [
                       {"key": "right_hand", "value": "יד ימין"},
                       {"key": "left_hand", "value": "יד שמאל"},
                       {"key": "right_leg", "value": "רגל ימין"},
                       {"key": "left_leg", "value": "רגל שמאל"},
                   ]
               },
               "blood_and_fluids": {
                   "key": "pre_hospital_fluids",
                   "title": "דם ונוזלים בשטח",
                   "values": [
                       {"key": "blood", "value": "דם"},
                       {"key": "plasma", "value": "פלזמה"},
                       {"key": "hartman", "value": "הרטמן"},
                       {"key": "cells", "value": "Packed cells"},
                   ]
               },
               "medications": {
                   "key": "pre_hospital_medications",
                   "title": "תרופות בשטח",
                   "values": [
                       {"key": "morphine", "value": "מורפיום (IV)", "subtitle": "Morphine"},
                       {"key": "actic", "value": "אקטיק", "subtitle": "Actic"},
                       {"key": "hexakapron", "value": "הקסקפרון", "subtitle": "Hexakapron"},
                       {"key": "neloxone", "value": "נלוקסון", "subtitle": "Neloxone"},
                   ],
                   "other": "אחר"
               },
               "vitals": {
                   "title": "מדדים בשטח",
                   "key": "pre_hospital_vitals",
                   "values": [
                       {"key": "systolic", "name": "SYS"},
                       {"key": "diastolic", "name": "DIA"},
                       {"key": "temperature", "name": "TEMP", "min": 35, "max": 42, "step": 0.1, "min_label": "35°>", "max_label": "42°"},
                       {"key": "pulse", "name": "PULSE"},
                       {"key": "saturation", "name": "SAT", "min": 60, "max": 100, "min_label": "60>"},
                   ]
               },
           },
       }},
   ],
}


async def init_views():
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'views',
        'version': 21,
        'value': [dict(
            index=0,
            name='אירוע רב נפגעים',
            short_name='אר"ן',
            key=MCI_DEPARTMENT,
            department_id=MCI_DEPARTMENT,
            type='department',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=NEW_MCI_VIEW,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=NEW_MCI_VIEW,
            ), dict(
                key='department',
                name='תצוגת אגפים',
                short_name='אגפים',
                panel_format=NEW_MCI_VIEW,
            )],
            default_mode='department',
        ), dict(
            index=1,
            name='המחלקה לרפואה דחופה',
            short_name='מלר"ד',
            key='1184000',
            department_id='1184000',
            type='department',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='department',
                name='תצוגת אגפים',
                short_name='אגפים',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='department',
        )] + [dict(
            index=index,
            name=MCI_NAMES.get(index, key),
            short_name=MCI_NAMES.get(index, key),
            key=f'{MCI_DEPARTMENT}-{key}',
            wing_id=key,
            department_id=MCI_DEPARTMENT,
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=NEW_MCI_VIEW,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=NEW_MCI_VIEW,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=NEW_MCI_VIEW,
            )],
            default_mode='status',
            **(dict(color=MCI_COLORS.get(index)) if MCI_COLORS.get(index) else {})
        ) for key, index in MCIIntakeWing.__members__.items()] + [dict(
            index=100,
            name='אגף 1',
            short_name='אגף 1',
            key='1184000-18',
            wing_id='18',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
            columns='1fr 1fr 1fr 1fr',
            rows='1fr 1fr 1fr 1fr',
            beds=[
                None, None, None, "13",
                "1", "6", "7", "12",
                "2", "5", "8", "11",
                "3", "4", "9", "10",
            ],
        ), dict(
            index=101,
            name='אגף 2',
            short_name='אגף 2',
            key='1184000-1',
            wing_id='1',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
            columns='1fr 1fr 1fr 1fr',
            rows='1fr 1fr 1fr 1fr',
            beds=[
                "14", None, None, "27",
                "15", "20", "21", "26",
                "16", "19", "22", "25",
                "17", "18", "23", "24",
            ],
        ), dict(
            index=102,
            name='אגף 3',
            short_name='אגף 3',
            key='1184000-3',
            wing_id='3',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
            columns='1fr 1fr 1fr 1fr',
            rows='1fr 1fr 1fr 1fr 1fr',
            beds=[
                None, None, None, "43",
                "28", "34", "35", "42",
                "29", "33", "36", "41",
                None, "32", "37", "40",
                "30", "31", "38", "39",
            ],
        ), dict(
            index=103,
            name='אגף 4',
            short_name='אגף 4',
            key='1184000-20',
            wing_id='20',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
        ), dict(
            index=104,
            name='אגף 5',
            short_name='אגף 5',
            key='1184000-26',
            wing_id='26',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
        ), dict(
            index=105,
            name='אגף הולכים',
            short_name='אגף הולכים',
            key='1184000-10',
            wing_id='10',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
        ), dict(
            index=99,
            name='חדר הלם',
            short_name='חדר הלם',
            key='1184000-17',
            wing_id='17',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
        ), dict(
            index=104,
            name='קליטה ראשונית',
            short_name='קליטה',
            key='1184000-wingless',
            wing_id='wingless',
            department_id='1184000',
            type='wing',
            modes=[dict(
                key='patients',
                name='תצוגת מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='layout',
                name='תצוגת מיקום',
                short_name='מיקום',
                panel_format=DEFAULT_PANEL_FORMAT,
            ), dict(
                key='status',
                name='תצוגת סטטוס',
                short_name='סטטוס',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='status',
        ), dict(
            index=201,
            name='מחלקת טראומה',
            short_name='טראומה',
            key=f"trauma",
            type='custom',
            modes=[dict(
                key='trauma',
                name='תצוגה סיכומית',
                short_name='סיכומי',
                panel_format=DEFAULT_PANEL_FORMAT,
            )],
            default_mode='trauma',
        ), dict(
            index=202,
            name='חדרי ניתוח',
            short_name='כירורגיה',
            key=f"surgical",
            type='custom',
            modes=[dict(
                key='patients',
                name='תצוגה מטופלים',
                short_name='מטופלים',
                panel_format=DEFAULT_MCI_PANEL_FORMAT,
            )],
            default_mode='patients',
        )]
    }).raise_for_status()
