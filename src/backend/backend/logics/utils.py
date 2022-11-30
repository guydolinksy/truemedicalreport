from typing import List


def prepare_update_object(path: List[str], value: any) -> dict:
    if not path:
        return value

    return {path[0]: prepare_update_object(path[1:], value)}
