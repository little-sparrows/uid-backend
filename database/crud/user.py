from typing import Optional, Iterable

from sqlalchemy import select, or_
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User


async def create_user(
        session: AsyncSession,
        fingerprint_id: str,
        weak_fingerprint_id: str,
        typing_dna_api_key: str,
) -> int:

    obj = User(
        fingerprint_id=fingerprint_id,
        weak_fingerprint_id=weak_fingerprint_id,
        typing_dna_api_key=typing_dna_api_key,
    )

    session.add(obj)
    await session.flush()
    await session.commit()

    return obj.id


async def get_user_by_id(
        session: AsyncSession,
        user_id: int
):

    obj = await session.get(User, user_id)

    return obj


async def identify_user(
        session: AsyncSession,
        fingerprint_id: str,
) -> Optional[User]:

    stmt = (select(User)
            .where(User.fingerprint_id == fingerprint_id))

    result = await session.execute(stmt)

    try:
        result = result.scalar_one_or_none()
    except MultipleResultsFound:
        return None

    return result


async def weak_identify_users(
        session: AsyncSession,
        weak_fingerprint_id: str,
) -> Iterable[User]:

    stmt = (select(User)
            .where(User.weak_fingerprint_id == weak_fingerprint_id))

    result = await session.execute(stmt)
    result = result.scalars()

    return result
