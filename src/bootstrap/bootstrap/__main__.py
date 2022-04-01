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
            ["1", None, "4", "7", None, "10"],
            ["2", None, "5", "8", None, "11"],
            ["3", None, "6", "9", None, "12"],
        ],
    })
    db.wings.insert_one({
        'name': 'אגף ב׳',
        'columns': [{'flex': '1'}, {'width': 50}, {'flex': '1'}, {'flex': '1'}, {'width': 50}, {'flex': '1'}],
        'rows': [{'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}],
        'beds': [
            ["13", None, "16, 19", None, "22"],
            ["14", None, "17, 20", None, "23"],
            ["15", None, "18, 21", None, "24"],
        ],
    })
    db.wings.insert_one({
        'name': 'אגף ג׳',
        'columns': [{'flex': '1'}, {'width': 50}, {'flex': '1'}, {'flex': '1'}, {'width': 50}, {'flex': '1'}],
        'rows': [{'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}, {'flex': '0 1'}],
        'beds': [
            ["25", None, "29, 33", None, "37"],
            ["26", None, "30, 34", None, "38"],
            ["27", None, "31, 35", None, "39"],
            ["28", None, "32, 36", None, "40"],
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
            'esi_score': {
                "value": bed_number % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            },
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
            'esi_score': {
                "value": i % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            },
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
            'esi_score': {
                "value": bed_number % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            }, 
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
            'esi_score': {
                "value": i % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            }, 'wing_id': db.wings.find_one({'name': 'אגף ב׳'})["_id"],
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
            'esi_score': {
                "value": bed_number % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            }, 
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
            'esi_score': {
                "value": i % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            },
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
            'esi_score': {
                "value": i % 5 + 1,
                "min": 3,
                "max": 5,
                "time": datetime.now().isoformat(),
                "is_live": False
            },
            'wing_id': db.wings.find_one({'name': 'אגף מהלכים'})["_id"],
            'bed': None,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (i == 3 or i == 8) else []
        })


init_wings()
init_patients()
