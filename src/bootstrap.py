import random
from datetime import datetime

from pymongo import MongoClient

db = MongoClient(host='medical-db', port=27017).tmr


def init_patients():
    db.patients.delete_many({})
    for bed_number in range(1, 13):
        if random.randint(1, 3) == 1:
            continue
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 37.2, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": bed_number % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'b1', 'bed': str(bed_number)},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if bed_number == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if bed_number == 8 else [])),
        })
    for i in range(0, 5):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 37.2, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": i % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'b1', 'bed': None},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if i == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if i == 8 else [])),
        })
    for bed_number in range(13, 25):
        if random.randint(1, 3) == 1:
            continue
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 37.5, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": bed_number % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'b2', 'bed': str(bed_number)},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if bed_number == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if bed_number == 8 else [])),
        })
    for i in range(0, 6):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 37.2, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": i % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'b2', 'bed': None},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if i == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if i == 8 else [])),
        })
    for bed_number in range(25, 41):
        if random.randint(1, 3) == 1:
            continue
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 37, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": bed_number % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'b3', 'bed': str(bed_number)},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if bed_number == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if bed_number == 8 else [])),
        })
    for i in range(0, 10):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 37.1, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": i % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'b3', 'bed': None},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if i == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if i == 8 else [])),
        })

    for i in range(0, 25):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'age': '70.2',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 36.9, "is_live": False, "min": 36.5, "max": 37.5,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 120,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "diastolic": {
                        "value": 80,
                        "min": 60,
                        "max": 100,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 60, "max": 90}
            },
            'severity': {
                "value": i % 5 + 1,
                "time": datetime.now().isoformat(),
            },
            'admission': {'department': 'er', 'wing': 'a', 'bed': None},
            'warnings': (([{'content': 'מחכה לך', 'severity': 2}] if i == 3 else []) +
                         ([{'content': 'טרופונין 18 מ״ג/ליטר', 'severity': 1}] if i == 8 else [])),
        })


init_patients()
