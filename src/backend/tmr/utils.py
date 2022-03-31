from typing import List


def prepare_update_object(path: List[str], value: any) -> dict:
    return {'.'.join(map(str, path)): value}
