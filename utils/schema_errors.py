from __future__ import annotations

from typing import Any, Optional, Dict, TypeVar

from fastapi.exceptions import HTTPException

_T = TypeVar("_T")


class HTTPExceptionWrapper(HTTPException):

    __status_code__: int = 400
    __detail__: str = 'error'
    __headers__: Optional[Dict[str, Any]] = None

    def __init__(
            self,
            status_code: int = None,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:

        status_code = status_code or self.__status_code__
        detail = detail or self.__detail__
        headers = headers or self.__headers__

        super().__init__(status_code=status_code, detail=detail, headers=headers)
