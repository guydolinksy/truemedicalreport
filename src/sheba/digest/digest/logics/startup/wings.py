import requests

from common.mci import MCI_DEPARTMENT, MCIIntakeWing, MCI_COLORS, MCI_NAMES
from digest import config


async def init_wings():
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'departments',
        'version': 11,
        'value': [{
            'index': 10,
            'name': 'אירוע רב נפגעים',
            'short_name': 'אר"ן',
            'key': MCI_DEPARTMENT,
        }, {
            'index': 9,
            'name': 'המחלקה לרפואה דחופה',
            'short_name': 'מלר"ד',
            'key': '1184000',
        }]
    }).raise_for_status()
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'wings',
        'version': 10,
        'value': [{
            'index': index,
            'key': key,
            'name': MCI_NAMES.get(index, key),
            'department': MCI_DEPARTMENT,
            'color': MCI_COLORS.get(index)
        } for key, index in MCIIntakeWing.__members__.items()] + [{
            'index': 10,
            'key': '18',
            'name': 'אגף 1',
            'department': '1184000',
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
            'index': 9,
            'key': '1',
            'name': 'אגף 2',
            'department': '1184000',
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
            'index': 8,
            'key': '3',
            'name': 'אגף 3',
            'department': '1184000',
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
            'index': 7,
            'key': '20',
            'name': 'אגף 4',
            'department': '1184000',
        }, {
            'index': 6,
            'key': '26',
            'name': 'אגף 5',
            'department': '1184000',
        }, {
            'index': 5,
            'key': '10',
            'name': 'אגף הולכים',
            'department': '1184000',
        }, {
            'index': 4,
            'key': '17',
            'name': 'חדר הלם',
            'department': '1184000',
        }]
    }).raise_for_status()
