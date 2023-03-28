from inspect import signature

import decorator
from fastapi.exceptions import HTTPException
from fastapi.params import Depends


class MaxRetriesExceeded(HTTPException):
    def __init__(self, msg: str) -> None:
        super().__init__(status_code=500, detail=msg)


class PatientNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404)


def inject_dependencies(**kwargs):
    @decorator.decorator
    def _wrapper(func):
        dependencies = {k: v.default for k, v in signature(func).parameters.items() if isinstance(v.default, Depends)}
        return func(**kwargs, **{k: v.dependency() for k, v in dependencies.items()})

    return _wrapper


def safe(logger):
    @decorator.decorator
    def _wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception('Safe run encountered an exception.')

    return _wrapper
