from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=message,
        )
