from typing import Optional

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=message,
        )


class ForbiddenException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=HTTP_403_FORBIDDEN,
            detail=message,
        )


class BadRequestException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail=message
        )


class InvalidSettingsException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message
