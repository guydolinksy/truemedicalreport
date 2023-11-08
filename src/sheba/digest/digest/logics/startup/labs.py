import requests

from digest import config


async def init_lab_categories():
    requests.post(f'{config.dal_url}/config/set', json={
        'key': 'lab_categories',
        'version': 10,
        'value': {
            "Therapeutic  Drugs": "Therapeutic Drugs",
        }
    }).raise_for_status()
