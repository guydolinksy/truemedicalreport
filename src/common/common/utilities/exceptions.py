from inspect import signature

import decorator
from fastapi.exceptions import HTTPException
from fastapi.params import Depends


class NotFoundException(HTTPException):
    def __init__(self, cls) -> None:
        super().__init__(status_code=404, detail=f'{cls} not found')


class PatientNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(cls='Patient')


class WingNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(cls='Wing')


class DepartmentNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(cls='Department')


class MaxRetriesExceeded(HTTPException):
    def __init__(self, msg: str) -> None:
        super().__init__(status_code=500, detail=msg)


def inject_dependencies(**presets):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            dependencies = {k: v.default for k, v in signature(func).parameters.items() if
                            isinstance(v.default, Depends)}
            return func(*args, **kwargs, **presets, **{k: v.dependency() for k, v in dependencies.items()})

        _wrapper.__name__ = func.__name__
        return _wrapper

    return _decorator


def safe(logger):
    @decorator.decorator
    def _wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.exception('Safe run encountered an exception.')

    return _wrapper
