from typing import Any, Dict, Optional

from fastapi.responses import JSONResponse


class BaseMessage:
    message = "Something unknown went wrong"
    status_code = 500
    code = "UNKNOWN"

    def __init__(self, message=None, status_code=None, code=None, **kwargs):
        self.message = str(message or self.message) % kwargs
        self.status_code = status_code or self.status_code
        self.code = code or self.code

    def json_serialize(self, extras: Optional[Dict[str, Any]] = None) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content={
                "message": str(self.message),
                "code": self.code,
                **(extras or {}),
            },
        )


class ClientError(BaseMessage, Exception):
    ...


class ServerError(BaseMessage, Exception):
    ...


class InternalServerError(ServerError):
    message = "Internal server error"
    status_code = 500
    code = "INTERNAL_SERVER_ERROR"


class OK(BaseMessage):
    message = "OK"
    status_code = 200
    code = "OK"


class BadRequest(ClientError):
    message = "Bad request"
    status_code = 400
    code = "BAD_REQUEST"


class Unauthorized(ClientError):
    message = "Unauthorized"
    status_code = 401
    code = "UNAUTHORIZED"


class Forbidden(ClientError):
    message = "Forbidden"
    status_code = 403
    code = "FORBIDDEN"


class NotFound(ClientError):
    message = "Not found"
    status_code = 404
    code = "NOT_FOUND"


class Conflict(ClientError):
    message = "Conflict"
    status_code = 409
    code = "CONFLICT"


class UnprocessableEntity(ClientError):
    message = "Unprocessable entity"
    status_code = 422
    code = "UNPROCESSABLE_ENTITY"


class SessionUnauthorized(Unauthorized):
    message = "Session unauthorized"
    code = "SESSION_UNAUTHORIZED"
