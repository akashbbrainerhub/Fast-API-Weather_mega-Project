from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail="Bad Request"):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(status_code=401, detail=detail)