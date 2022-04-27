import requests


def load_notification(department, wing):
    res = requests.get(f"http://medical-dal/medical-dal/departments/{department}/wings/{wing}/notifications").json()
    return res
