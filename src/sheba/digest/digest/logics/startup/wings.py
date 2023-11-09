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
        'version': 12,
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
            'columns': '1fr 1fr 1fr 1fr',
            'rows': '1fr 1fr 1fr 1fr',
            'beds': [
                None, None, None, "13",
                "1", "6", "7", "12",
                "2", "5", "8", "11",
                "3", "4", "9", "10",
            ],
        }, {
            'index': 9,
            'key': '1',
            'name': 'אגף 2',
            'department': '1184000',
            'columns': '1fr 1fr 1fr 1fr',
            'rows': '1fr 1fr 1fr 1fr',
            'beds': [
                "14", None, None, "27",
                "15", "20", "21", "26",
                "16", "19", "22", "25",
                "17", "18", "23", "24",
            ],
        }, {
            'index': 8,
            'key': '3',
            'name': 'אגף 3',
            'department': '1184000',
            'columns': '1fr 1fr 1fr 1fr',
            'rows': '1fr 1fr 1fr 1fr 1fr',
            'beds': [
                None, None, None, "43",
                "28", "34", "35", "42",
                "29", "33", "36", "41",
                None, "32", "37", "40",
                "30", "31", "38", "39",
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
