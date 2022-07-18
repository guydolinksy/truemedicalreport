from datetime import datetime
import pytz


def calculate_patient_age(birthdate) -> str:
    stringify_age: str
    try:
        date_diff = datetime.utcnow() - birthdate
        stringify_age = f"{int(date_diff.days / 365)}.{int((date_diff.days % 365) / 30)}"
    except TypeError:
        stringify_age = ""
    return stringify_age


def datetime_utc_serializer(datetime_object):
    serialized: str | None
    try:
        serialized = datetime_object.astimezone(pytz.UTC).isoformat()
    except AttributeError:
        serialized = None
