import requests

from .. import config


async def init_wings():
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'departments',
        'version': 1,
        'value': [{
            'name': 'er',
            'key': 1184000,
            'wings': [{
                'key': 'אגף B1',
                'name': 'אגף 1',
                'department': 'er',
                'columns': [
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 1, 'minWidth': 16},
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 2, 'minWidth': 128},
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 1, 'minWidth': 16},
                    {'flex': "4 1 300px", 'minWidth': 300}
                ],
                'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'},
                         {'height': 16},
                         {'flex': '0 1'}],
                'beds': [
                    [None, None, None, None, None, None, "13"],
                    [None] * 7,
                    ["1", None, "6", None, "7", None, "12"],
                    [None] * 7,
                    ["2", None, "5", None, "8", None, "11"],
                    [None] * 7,
                    ["3", None, "4", None, "9", None, "10"],
                ],
            }, {
                'key': 'אגף B2',
                'name': 'אגף 2',
                'department': 'er',
                'columns': [
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 1, 'minWidth': 16},
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 2, 'minWidth': 128},
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 1, 'minWidth': 16},
                    {'flex': "4 1 300px", 'minWidth': 300}
                ],
                'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'},
                         {'height': 16},
                         {'flex': '0 1'}],
                'beds': [
                    ["14", None, None, None, None, None, "27"],
                    [None] * 7,
                    ["15", None, "20", None, "21", None, "26"],
                    [None] * 7,
                    ["16", None, "19", None, "22", None, "25"],
                    [None] * 7,
                    ["17", None, "18", None, "23", None, "24"],
                ],
            }, {
                'key': 'אגף B3',
                'name': 'אגף 3',
                'department': 'er',
                'columns': [
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 1, 'minWidth': 16},
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 2, 'minWidth': 128},
                    {'flex': "4 1 300px", 'minWidth': 300},
                    {'flex': 1, 'minWidth': 16},
                    {'flex': "4 1 300px", 'minWidth': 300}
                ],
                'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'},
                         {'height': 16},
                         {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}],
                'beds': [
                    [None, None, None, None, None, None, "43"],
                    [None] * 7,
                    ["28", None, "34", None, "35", None, "42"],
                    [None] * 7,
                    ["29", None, "33", None, "36", None, "41"],
                    [None] * 7,
                    [None, None, "32", None, "37", None, "40"],
                    [None] * 7,
                    ["30", None, "31", None, "38", None, "39"],
                ],
            }, {
                'key': 'אגף B4',
                'name': 'אגף 4',
                'department': 'er',
                'blocks': []
            }, {
                'key': 'אגף הולכים',
                'name': 'אגף הולכים',
                'department': 'er',
                'blocks': []
            }, {
                'key': 'חדר הלם',
                'name': 'חדר הלם',
                'department': 'er',
                'blocks': []
            }]
        }]
    }).raise_for_status()


async def init_protocols():
    # Common values
    CXR_KEYS = [
                    'imaging-צילום בית החזה בעמידה',
                    'imaging-צילום בית החזה בשכיבה/ישיבה',
                    'imaging-צילום חזה+צבס',
                ]
    HCT_KEYS = [
                    'imaging-CT מוח לבירור שבץ-מוחי',
                    'imaging-CT מוח',
                    'imaging-CTA פרוטוקול פרפוזיה כולל מח ואנגיו צוואר ומוח'
                ]
    US_STOMACH_KEYS = ['imaging-US בטן']
    TRPONIN_KEYS = ['lab-120104040']
    HGB_KEYS = ['lab-100109497']
    CRP_KEYS = ['lab-120104016']
    WBC_KEYS = ['lab-100109500']
    TEMPERATURE_KEYS = ['measure-temperature']
    SATURATION_KEYS = ['measure-saturation']

    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'protocols',
        'version': 2,
        'value': {
            'כאב חזה': [
                {'name': 'צילום חזה', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': CXR_KEYS},
                {'name': 'טרופונין', 'default': '-', 'key': 'lab-1', 'keys': TRPONIN_KEYS},
            ],
            'סינקופה': [
                {'name': 'טרופונין', 'default': '-', 'key': 'lab-1', 'keys': TRPONIN_KEYS},
                {'name': 'HGB', 'default': '-', 'key': 'lab-2', 'keys': HGB_KEYS},
            ],
            'חום': [
                {'name': 'CRP', 'default': '-', 'key': 'lab-1', 'keys': CRP_KEYS},
                {'name': 'WBC', 'default': '-', 'key': 'lab-2', 'keys': WBC_KEYS},
                {'name': 'לקטט', 'default': '-', 'key': 'lab-3', 'keys': ['lab-150108685']},
            ],
            'תלונה נוירולוגית': [
                {'name': 'CT ראש', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
            ],
            'חבלה/נפילה': [
                {'name': 'CT מוח בלי חומר ניגוד', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
                {'name': 'צילום אגן', 'default': 'לא הוזמן', 'key': 'img-2', 'keys': ['imaging-צילום אגן/אגן וירך']},
                {'name': 'צילום חזה', 'default': 'לא הוזמן', 'key': 'img-3', 'keys': CXR_KEYS},
            ],
            'דימום מדרכי עיכול': [
                {'name': 'המוגלובין', 'default': '-', 'key': 'lab-1', 'keys': HGB_KEYS + ['lab-100107943']},
            ],
            'לאחר פרכוס': [
                {'name': 'CT מוח', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
                {'name': 'Total CPK', 'default': '-', 'key': 'lab-1', 'keys': ['lab-100182550']},
            ],
            'קוצר נשימה': [
                {'name': 'צילום חזה', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': CXR_KEYS},
                {'name': 'pco2', 'default': '-', 'key': 'lab-1', 'keys': ['lab-152808699']},
                {'name': 'ph', 'default': '-', 'key': 'lab-2', 'keys': ['lab-152808700']},
                {'name': 'hco3', 'default': '-', 'key': 'lab-3', 'keys': ['lab-152808697']},
                {'name': 'טרופונין', 'default': '-', 'key': 'lab-4', 'keys': TRPONIN_KEYS},
            ],
            'תלונות א.א.ג': [
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
                {'name': 'חום', 'default': '-', 'key': 'measure-1', 'keys': TEMPERATURE_KEYS},
                {'name': 'סטורציה', 'default': '-', 'key': 'measure-2', 'keys': SATURATION_KEYS},
            ],
            'חשד לבקע': [
                {'name': 'US כליות ודרכי שתן', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': ['imaging-US כליות ודרכי שתן']},
                {'name': 'US בטן', 'default': 'לא הוזמן', 'key': 'img-2', 'keys': US_STOMACH_KEYS},
                {'name': 'US ורידי הגפיים התחתונות כולל דופלר', 'default': 'לא הוזמן', 'key': 'img-2', 'keys': ['imaging-US ורידי הגפיים התחתונות כולל דופלר']},
            ],
            'סחרחורת': [
                {'name': 'CT מוח', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
                {'name': 'HGB', 'default': '-', 'key': 'lab-1', 'keys': HGB_KEYS},
            ],
            'כאב בטן': [
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
                {'name': 'US בטן', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': US_STOMACH_KEYS},
            ],
            'תלונות לאחר ניתוח': [
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
                {'name': 'HGB', 'default': '-', 'key': 'lab-3', 'keys': HGB_KEYS},
            ],
            'כאבי ראש': [
                {'name': 'CT מוח', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
            ],
            'תאונת דרכים': [
                {'name': 'CT עמוד שדרה צוארי', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': ['CT עמוד שדרה צוארי']},
            ],
        }
    }).raise_for_status()


async def init_lab_categories():
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'lab_categories',
        'version': 0,
        'value': {
            "Therapeutic  Drugs": "Therapeutic Drugs",
        }
    }).raise_for_status()


async def startup():
    await init_wings()
    await init_protocols()
    await init_lab_categories()
