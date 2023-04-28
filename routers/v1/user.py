import asyncio
from typing import Union

from loguru import logger

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from auth import auth_admin

from database import crud
from database import exceptions as database_exceptions
from schemas.v1 import user as user_schemas
from schemas.v1.extra import msg_responses, err_responses

from utils.typing_dna import typing_dna, Action, Responses, get_current_dna_api_key

from ..common import database_session, SessionType


router = APIRouter()


@router.get(
    "/check"
)
async def check_user(
        session: SessionType = Depends(database_session),
        fingerprint_id: str = ...,
        weak_fingerprint_id: str = ...,
        collected_typing_patterns: list[str] = Query(default=[]),
) -> int:
    """Check user endpoint

    Requires fingerprint identifier. Optionally, you
    can provide collecting typing patterns, which may
    make result more accurate.

    Returns information about User, that was defined as related
    to the provided identifier. If user not found in database,
    it will be created automatically.

    """

    exact_id_user = await crud.user.identify_user(
        session,
        fingerprint_id=fingerprint_id,
    )

    if exact_id_user is None:
        exact_id_user_id = await crud.user.create_user(
            session,
            fingerprint_id=fingerprint_id,
            weak_fingerprint_id=weak_fingerprint_id,
            typing_dna_api_key=get_current_dna_api_key(),
        )
        exact_id_user = await crud.user.get_user_by_id(
            session,
            exact_id_user_id
        )

    if not collected_typing_patterns:
        return exact_id_user.id

    weak_id_users = await crud.user.weak_identify_users(
        session,
        weak_fingerprint_id,
    )

    if exact_id_user not in weak_id_users:
        logger.error(f"identifiers conflict at user `{exact_id_user.id}`. "
                     f"the set of users with provided weak identifier "
                     f"`{weak_fingerprint_id}` not contains that user. check"
                     f" out identifiers evaluating methods on your side.")
        return exact_id_user.id

    weak_id_users_ids = [i.id for i in weak_id_users]

    typing_check_results: tuple[Responses.Auto]

    # noinspection PyTypeChecker
    typing_check_results = await asyncio.gather(
        *(typing_dna.verify_typing_pattern(
             i,
             collected_typing_patterns,
             str(i.id)
         ) for i in weak_id_users_ids)
    )

    typing_check_result_exact = await typing_dna.auto(
        user_identifier=exact_id_user.fingerprint_id,
        typing_patterns=collected_typing_patterns,
    )

    if isinstance(typing_check_result_exact, Responses.Error):
        logger.error(f"error from typing_dna while tried to send auto request for "
                     f"user `{exact_id_user.id}`. error info: {typing_check_result_exact}")

    verified_users_ids = []

    for i_user_id, i in zip(weak_id_users_ids, typing_check_results):
        if isinstance(i, Responses.Error):
            logger.error(f"error from typing_dna while tried to verify user's typing pattern "
                         f"`{i_user_id}`. error info: {i}")
            return exact_id_user.id
        if i.action is Action.enroll:
            logger.error(f"algorithm expects that auto-enroll is off for request `verify_typing_pattern`,"
                         f"but action `{i.action}` got.")
            return exact_id_user.id
        elif i.action is Action.verify_and_enroll:
            logger.warning(f"algorithm expects that auto-enroll is off for request `verify_typing_pattern`,"
                           f"but action `{i.action}` got.")
            verified_users_ids.append(i.message_code)
        elif i.action is Action.verify:
            verified_users_ids.append(i.message_code)
        else:
            raise KeyError(f"Unknown action {i.action}")

    logger.debug(f"{len(verified_users_ids)} of {len(typing_check_results)} weak_id users are verified")

    if not verified_users_ids:

        # if not users determined by checking
        result = await crud.user.identify_user(
            session,
            fingerprint_id=fingerprint_id
        )
    elif len(verified_users_ids) == 1:

        # if dna determined exact one user, we
        # scip checking fingerprint_id.

        result = await crud.user.get_user_by_id(
            session,
            user_id=verified_users_ids[0]
        )

        is_match = result.id == exact_id_user.id

        logger.debug(f"dna check result are {'' if is_match else 'not '}"
                     f"match with exact fingerprint for user {result.id}"
                     f"{'' if is_match else f' and {exact_id_user.id}'}")

    else:
        # dna check failed

        logger.debug(f'dna check is failed for user {exact_id_user.id}')
        result = exact_id_user

    return result.id
