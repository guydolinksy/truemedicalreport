import requests

from .. import config


async def init_wings():
    requests.post(f'{config.dal_url}/init/wings', json={'wings':
        [{
            'key': 'אגף B1',
            'name': 'אגף א׳',
            'department': 'er',
            'columns': [
                {'flex': "4 1 300px", 'minWidth': 300},
                {'width': 16, 'minWidth': 16},
                {'flex': "4 1 300px", 'minWidth': 300},
                {'flex': 1, 'minWidth': 32},
                {'flex': "4 1 300px", 'minWidth': 300},
                {'width': 16, 'minWidth': 16},
                {'flex': "4 1 300px", 'minWidth': 300}
            ],
            'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16},
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
            'rows': [{'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16}, {'flex': '0 1'}, {'height': 16},
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
            'key': 'אגף הולכים',
            'name': 'אגף הולכים',
            'department': 'er',
            'blocks': []
        }, {
            'key': 'חדר הלם',
            'name': 'חדר הלם',
            'department': 'er',
            'blocks': []
        }]}).raise_for_status()


async def startup():
    await init_wings()
