import asyncio
from inspect import signature

from fastapi.exceptions import HTTPException
from fastapi.params import Depends


class MaxRetriesExceeded(HTTPException):
    def __init__(self, msg: str) -> None:
        super().__init__(status_code=500, detail=msg)


class PatientNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404)


def inject_dependencies(**kwargs):
    def _decorator(func):
        dependencies = {k: v.default for k, v in signature(func).parameters.items() if isinstance(v.default, Depends)}

        if asyncio.iscoroutinefunction(func):
            async def _wrapper():
                return await func(**kwargs, **{k: v.dependency() for k, v in dependencies.items()})
        else:
            def _wrapper():
                return func(**kwargs, **{k: v.dependency() for k, v in dependencies.items()})

        return _wrapper

    return _decorator


def safe(logger):
    def _decorator(func):

        if asyncio.iscoroutinefunction(func):
            async def _wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    logger.exception('Safe run encountered an exception.')
        else:
            def _wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logger.exception('Safe run encountered an exception.')
        return _wrapper

    return _decorator
