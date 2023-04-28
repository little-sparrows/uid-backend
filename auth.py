from fastapi import Query

from config import environment
from schemas.v1.extra.err_responses import Exceptions


async def auth_admin(access_token: str = Query()):
    if access_token != environment.auth_access_token:
        raise Exceptions.PermissionDenied()


async def auth_public():
    pass
