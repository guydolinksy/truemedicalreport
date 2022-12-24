from inspect import signature
from fastapi.params import Depends
from fastapi.exceptions import HTTPException


class MaxRetriesExceeded(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=500)


class PatientNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404)


def inject_dependencies(**kwargs):
    def _decorator(func):
        dependencies = {k: v.default for k, v in signature(func).parameters.items() if isinstance(v.default, Depends)}

        async def _wrapper():
            return await func(**kwargs, **{k: v.dependency() for k, v in dependencies.items()})

        return _wrapper

    return _decorator


def safe(logger):
    def _decorator(func):
        async def _wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                logger.exception('Safe run encountered an exception.')

        return _wrapper

    return _decorator
