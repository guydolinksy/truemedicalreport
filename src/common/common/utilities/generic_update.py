from pydantic import BaseModel


def index_by_key(list, key):
    for i in range(len(list)):
        if ((isinstance(list[i], BaseModel) and list[i].key == key) or
                (isinstance(list[i], dict) and list[i]['key'] == key)):
            return i


def generic_update(prev, path, value):
    obj = prev
    for part in path[:-1]:
        if isinstance(obj, BaseModel):
            obj = getattr(obj, part)
        elif isinstance(obj, dict):
            obj = obj[part]
        elif isinstance(obj, list):
            obj = obj[index_by_key(obj, part)]

    if isinstance(obj, BaseModel):
        setattr(obj, path[-1], value)
    elif isinstance(obj, dict):
        obj[path[-1]] = value
    elif isinstance(obj, list):
        if not value:
            if (i := index_by_key(obj, path[-1])) is not None:
                obj.remove(obj[i])
        else:
            if (i := index_by_key(obj, path[-1])) is not None:
                obj[i] = value
            else:
                obj.append(value)
