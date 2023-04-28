from sqlalchemy.ext.asyncio import AsyncSession

from database.database import engine


async def database_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
