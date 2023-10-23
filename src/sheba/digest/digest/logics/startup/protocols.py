import requests

from ... import config


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
        'version': 10,
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
            'ספסיס': [
                {'name': 'CRP', 'default': '-', 'key': 'lab-1', 'keys': CRP_KEYS},
                {'name': 'WBC', 'default': '-', 'key': 'lab-2', 'keys': WBC_KEYS},
                {'name': 'לקטט', 'default': '-', 'key': 'lab-3', 'keys': ['lab-150108685']},
                {'name': 'חום', 'default': '-', 'key': 'measure-1', 'keys': TEMPERATURE_KEYS},
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
                {'name': 'US כליות ודרכי שתן', 'default': 'לא הוזמן', 'key': 'img-1',
                 'keys': ['imaging-US כליות ודרכי שתן']},
                {'name': 'US בטן', 'default': 'לא הוזמן', 'key': 'img-2', 'keys': US_STOMACH_KEYS},
                {'name': 'US ורידי הגפיים התחתונות כולל דופלר', 'default': 'לא הוזמן', 'key': 'img-2',
                 'keys': ['imaging-US ורידי הגפיים התחתונות כולל דופלר']},
            ],
            'סחרחורת': [
                {'name': 'CT מוח', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
                {'name': 'HGB', 'default': '-', 'key': 'lab-1', 'keys': HGB_KEYS},
            ],
            'כאבי בטן': [
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
                {'name': 'US בטן', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': US_STOMACH_KEYS},
            ],
            'תלונות לאחר ניתוח': [
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
                {'name': 'HGB', 'default': '-', 'key': 'lab-3', 'keys': HGB_KEYS},
            ],
            'צלוליטיס': [
                {'name': 'WBC', 'default': '-', 'key': 'lab-1', 'keys': WBC_KEYS},
                {'name': 'CRP', 'default': '-', 'key': 'lab-2', 'keys': CRP_KEYS},
                {'name': 'חום', 'default': '-', 'key': 'measure-1', 'keys': TEMPERATURE_KEYS},
            ],
            'חשד לשבץ מוחי טרי': [
                {'name': 'CT מוח', 'default': 'לא הוזמן', 'key': 'img-1', 'keys': HCT_KEYS},
            ],
            'חולשה': [
                {'name': 'טרופונין', 'default': '-', 'key': 'lab-1', 'keys': TRPONIN_KEYS},
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
