from typing import Any

from litestar.exceptions import HTTPException
from litestar import status_codes as status


class BaseHTTPException(HTTPException):
    headers = {"Content-Type": "application/json"}

    def __init__(self, extra: dict[str, Any] = None) -> None:
        super().__init__(
            detail=self.detail,
            status_code=self.status_code,
            headers=self.headers,
            extra=extra,
        )


class NotFoundSpeakerHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Speaker not found"


class NotCorrectTextHTTPException(BaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Text is not correct"


class TextTooLongHTTPException(BaseHTTPException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    detail = "Text too long"


class InvalidSampleRateHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid sample rate"


genetate_exceptions = [
    NotFoundSpeakerHTTPException,
    NotCorrectTextHTTPException,
    TextTooLongHTTPException,
    InvalidSampleRateHTTPException,
]
