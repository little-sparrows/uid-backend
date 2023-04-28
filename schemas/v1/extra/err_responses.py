from typing import Literal

from fastapi import status
from pydantic import BaseModel

from utils.schema_errors import HTTPExceptionWrapper


class Exceptions:
    class PermissionDenied(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_403_FORBIDDEN
        __detail__ = 'permission denied'


class Schemas:
    class PermissionDenied(BaseModel):
        detail: Literal['permission denied']
