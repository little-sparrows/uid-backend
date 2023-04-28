from typing_extensions import TypeAlias
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import engine


SessionType: TypeAlias = AsyncSession


async def database_session() -> AsyncGenerator[SessionType, None]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
