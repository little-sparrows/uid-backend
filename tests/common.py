import time

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base
from database.database import engine

from config import environment


@pytest.fixture(scope="session", autouse=True)
def fx_check_if_testing_allowed():
    if not environment.allow_testing:
        raise RuntimeError(f"Testing is not allowed. {environment.ALLOW_TESTING=}")


@pytest_asyncio.fixture(scope="function")
async def fx_db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    await engine.dispose()


__all__ = ['fx_check_if_testing_allowed', 'fx_db_session']
