from typing import Literal

from fastapi import status
from pydantic import Field

from schemas.v1.base import NoContentResponse


class Ok(NoContentResponse):
    _status_code_ = Field(status.HTTP_200_OK, const=True)

    message: Literal['ok'] = 'ok'
