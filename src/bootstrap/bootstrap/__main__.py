from pymongo import MongoClient
from bson import objectid

db = MongoClient(host='medical-db').tmr


def init_wings():
    db.wings.delete_many({})
    db.wings.insert_one({
        'name': 'אגף א׳',
        'blocks': [{
            'name': 'מסדרון ימין',
            'sides': [
                {'name': 'צד ימין', 'beds': [1, 2, 3, 4]},
                {'name': 'צד שמאל', 'beds': [5, 6, 7, 8]},
            ]
        }, {
            'name': 'מסדרון שמאל',
            'sides': [
                {'name': 'צד ימין', 'beds': [9, 10, 11, 12]},
                {'name': 'צד שמאל', 'beds': [13, 14, 15, 16]},
            ]
        }]
    })
    db.wings.insert_one({
        'name': 'אגף ב׳',
        'blocks': [{
            'name': 'מסדרון ימין',
            'sides': [
                {'name': 'צד ימין', 'beds': [17, 18, 19, 20]},
                {'name': 'צד שמאל', 'beds': [21, 22, 23, 24]},
            ]
        }, {
            'name': 'מסדרון שמאל',
            'sides': [
                {'name': 'צד ימין', 'beds': [25, 26, 27, 28]},
                {'name': 'צד שמאל', 'beds': [29, 30, 31, 32]},
            ]
        }]
    })
    db.wings.insert_one({
        'name': 'אגף ג׳',
        'blocks': [{
            'name': 'מסדרון ימין',
            'sides': [
                {'name': 'צד ימין', 'beds': [33, 34, 35, 36]},
                {'name': 'צד שמאל', 'beds': [37, 38, 39, 40]},
            ]
        }, {
            'name': 'מסדרון שמאל',
            'sides': [
                {'name': 'צד ימין', 'beds': [41, 42, 43, 44]},
                {'name': 'צד שמאל', 'beds': [45, 46, 47, 48]},
            ]
        }]
    })


def init_patients():
    db.patients.delete_many({})
    for bed_number in range(1, 17):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awating': 'פענוח סיטי',
            'flagged': False,
            'loading': 'פענוח סיטי',
            'measures': {'pulse': 80, 'blood_pressure': "140/80", 'temperature': 38},
            'wing_id': db.wings.find_one({'name': 'אגף א׳'})["_id"],
            'bed': bed_number,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (bed_number == 8 or bed_number == 5) else []
        })
    for bed_number in range(17, 33):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awating': 'פענוח סיטי',
            'flagged': False,
            'loading': 'פענוח סיטי',
            'measures': {'pulse': 80, 'blood_pressure': "140/80", 'temperature': 38},
            'wing_id': db.wings.find_one({'name': 'אגף ב׳'})["_id"],
            'bed': bed_number,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (bed_number == 25 or bed_number == 19) else []
        })
    for bed_number in range(33, 49):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awating': 'פענוח סיטי',
            'flagged': False,
            'loading': 'פענוח סיטי',
            'measures': {'pulse': 80, 'blood_pressure': "140/80", 'temperature': 38},
            'wing_id': db.wings.find_one({'name': 'אגף ג׳'})["_id"],
            'bed': bed_number,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (bed_number == 38 or bed_number == 45) else []
        })
    for i in range(0, 10):
        db.patients.insert_one({
            'name': 'ישראל ישראלי',
            'complaint': 'קוצר נשימה',
            'awating': 'פענוח סיטי',
            'flagged': False,
            'loading': 'פענוח סיטי',
            'measures': {'pulse': 80, 'blood_pressure': "140/80", 'temperature': 38},
            'wing_id': db.wings.find_one({'name': 'אגף ג׳'})["_id"],
            'bed_num': None,
            'warnings': ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] if (i == 3 or i == 8) else []
        })


init_wings()
init_patients()
