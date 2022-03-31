from pymongo import MongoClient
from bson import objectid
from datetime import datetime

db = MongoClient(host='medical-db').tmr


def init_wings():
    db.wings.delete_many({})
    db.wings.insert_one({
        'name': 'אגף א׳',
        'columns': [{'flex': '1'}, {'width': 50}, {'flex': '1'}, {'flex': '1'}, {'width': 50}, {'flex': '1'}],
        'rows': [{'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}],
        'beds': [
            [1, 0, 4, 7, 0, 10],
            [2, 0, 5, 8, 0, 11],
            [3, 0, 6, 9, 0, 12],
        ],
    })
    db.wings.insert_one({
        'name': 'אגף ב׳',
        'columns': [{'flex': '1'}, {'width': 50}, {'flex': '1'}, {'flex': '1'}, {'width': 50}, {'flex': '1'}],
        'rows': [{'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}],
        'beds': [
            [13, 0, 16, 19, 0, 22],
            [14, 0, 17, 20, 0, 23],
            [15, 0, 18, 21, 0, 24],
        ],
    })
    db.wings.insert_one({
        'name': 'אגף ג׳',
        'columns': [{'flex': '1'}, {'width': 50}, {'flex': '1'}, {'flex': '1'}, {'width': 50}, {'flex': '1'}],
        'rows': [{'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}],
        'beds': [
            [25, 0, 29, 33, 0, 37],
            [26, 0, 30, 34, 0, 38],
            [27, 0, 31, 35, 0, 39],
            [28, 0, 32, 36, 0, 40],
        ],
    })
    db.wings.insert_one({
        'name': 'אגף מהלכים',
        'blocks': []
    })


def init_patients():
    db.patients.delete_many({})
    for bed_number in range(1, 13):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 38, "is_live": False, "min": 24.3, "max": 39.1,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "dyastolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 42, "max": 200}
            },
            'esiScore': bed_number % 5,
            'wing_id': db.wings.find_one({'name': 'אגף א׳'})["_id"],
            'bed': str(bed_number),
            # 'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (bed_number == 8 or bed_number == 5) else []
        })
    for i in range(0, 5):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {'pulse': 80, 'bloodPressure': "140/80", 'temperature': 38},
            'esiScore': i % 5,
            'wing_id': db.wings.find_one({'name': 'אגף א׳'})["_id"],
            'bed': None,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (i == 3 or i == 8) else []
        })
    for bed_number in range(13, 25):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 38, "is_live": False, "min": 24.3, "max": 39.1,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "dyastolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 42, "max": 200}
            },
            'esiScore': bed_number % 5,
            'wing_id': db.wings.find_one({'name': 'אגף ב׳'})["_id"],
            'bed': str(bed_number),
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (bed_number == 25 or bed_number == 19) else []
        })
    for i in range(0, 6):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {'pulse': 80, 'bloodPressure': "140/80", 'temperature': 38},
            'esiScore': i % 5,
            'wing_id': db.wings.find_one({'name': 'אגף ב׳'})["_id"],
            'bed': None,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (i == 3 or i == 8) else []
        })
    for bed_number in range(25, 41):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 38, "is_live": False, "min": 24.3, "max": 39.1,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "dyastolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 42, "max": 200}
            },
            'esiScore': bed_number % 5,
            'wing_id': db.wings.find_one({'name': 'אגף ג׳'})["_id"],
            'bed': str(bed_number),
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (bed_number == 38 or bed_number == 45) else []
        })
    for i in range(0, 10):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 38, "is_live": False, "min": 24.3, "max": 39.1,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "dyastolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 42, "max": 200}
            },
            'esiScore': i % 5,
            'wing_id': db.wings.find_one({'name': 'אגף ג׳'})["_id"],
            'bed': None,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (i == 3 or i == 8) else []
        })

    for i in range(0, 25):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awaiting': 'פענוח סיטי',
            'flagged': False,
            'measures': {
                "temperature": {"value": 38.2, "is_live": False, "min": 24.3, "max": 39.1,
                                "time": datetime.now().isoformat()},
                "blood_pressure": {
                    "systolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    },
                    "dyastolic": {
                        "value": 140,
                        "min": 90,
                        "max": 190,
                        "time": datetime.now().isoformat(),
                        "is_live": False
                    }
                },
                "pulse": {"value": 80, "is_live": False, "time": datetime.now().isoformat(), "min": 42, "max": 200}
            },
            'esiScore': i % 5,
            'wing_id': db.wings.find_one({'name': 'אגף מהלכים'})["_id"],
            'bed': None,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (i == 3 or i == 8) else []
        })


init_wings()
init_patients()
