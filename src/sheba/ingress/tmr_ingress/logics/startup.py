from pymongo import MongoClient


async def init_wings():
    client = MongoClient(host='mongo')
    client.drop_database('medical')

    db = client.medical
    db.wings.delete_many({})
    db.wings.insert_one({
        'key': 'b1',
        'name': 'אגף א׳',
        'department': 'er',
        'columns': [
            {'flex': "4 1 300px", 'minWidth': 300},
            {'flex': 1, 'minWidth': 32},
            {'flex': "4 1 300px", 'minWidth': 300},
            {'width': 16, 'minWidth': 16},
            {'flex': "4 1 300px", 'minWidth': 300},
            {'flex': 1, 'minWidth': 32},
            {'flex': "4 1 300px", 'minWidth': 300}
        ],
        'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}],
        'beds': [
            ["1", None, "4", None, "7", None, "10"],
            [None] * 7,
            ["2", None, "5", None, "8", None, "11"],
            [None] * 7,
            ["3", None, "6", None, "9", None, "12"],
        ],
    })
    db.wings.insert_one({
        'key': 'b2',
        'name': 'אגף ב׳',
        'department': 'er',
        'columns': [
            {'flex': "4 1 300px", 'minWidth': 300},
            {'flex': 1, 'minWidth': 32},
            {'flex': "4 1 300px", 'minWidth': 300},
            {'width': 16, 'minWidth': 16},
            {'flex': "4 1 300px", 'minWidth': 300},
            {'flex': 1, 'minWidth': 32},
            {'flex': "4 1 300px", 'minWidth': 300}
        ],
        'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}],
        'beds': [
            ["13", None, "16", None, "19", None, "22"],
            [None] * 7,
            ["14", None, "17", None, "20", None, "23"],
            [None] * 7,
            ["15", None, "18", None, "21", None, "24"],
        ],
    })
    db.wings.insert_one({
        'key': 'b3',
        'name': 'אגף ג׳',
        'department': 'er',
        'columns': [
            {'flex': "4 1 300px", 'minWidth': 300},
            {'flex': 1, 'minWidth': 32},
            {'flex': "4 1 300px", 'minWidth': 300},
            {'width': 16, 'minWidth': 16},
            {'flex': "4 1 300px", 'minWidth': 300},
            {'flex': 1, 'minWidth': 32},
            {'flex': "4 1 300px", 'minWidth': 300}
        ],
        'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16},
                 {'flex': '0 1'}],
        'beds': [
            ["25", None, "29", None, "33", None, "37"],
            [None] * 7,
            ["26", None, "30", None, "34", None, "38"],
            [None] * 7,
            ["27", None, "31", None, "35", None, "39"],
            [None] * 7,
            ["28", None, "32", None, "36", None, "40"],
        ],
    })
    db.wings.insert_one({
        'key': 'a',
        'name': 'אגף מהלכים',
        'department': 'er',
        'blocks': []
    })
    db.wings.insert_one({
        'key': 'S',
        'name': 'חדר הלם',
        'department': 'er',
        'blocks': []
    })


async def startup():
    await init_wings()
