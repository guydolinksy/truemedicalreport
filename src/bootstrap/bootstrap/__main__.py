from pymongo import MongoClient

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
                {'name': 'צד ימין', 'beds': [25, 26, 26, 27]},
                {'name': 'צד שמאל', 'beds': [28, 29, 30, 31]},
            ]
        }]
    })
    db.wings.insert_one({
        'name': 'אגף ג׳',
        'blocks': [{
            'name': 'מסדרון ימין',
            'sides': [
                {'name': 'צד ימין', 'beds': [32, 33, 34, 35]},
                {'name': 'צד שמאל', 'beds': [36, 37, 38, 39]},
            ]
        }, {
            'name': 'מסדרון שמאל',
            'sides': [
                {'name': 'צד ימין', 'beds': [40, 41, 42, 43]},
                {'name': 'צד שמאל', 'beds': [44, 45, 46, 47]},
            ]
        }]
    })


init_wings()
