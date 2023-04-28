from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from config import environment


def _create_engine(driver: str, is_async: bool):
    if is_async:
        create = create_async_engine
    else:
        create = create_engine

    engine_ = create(
        'postgresql+{}://{}:{}@{}:{}/{}'.format(
            driver,
            environment.postgres_user,
            environment.postgres_password,
            environment.postgres_host,
            environment.postgres_port,
            environment.postgres_db
        )
    )

    return engine_


engine = _create_engine('asyncpg', is_async=True)
sync_engine = _create_engine('psycopg2', is_async=False)
