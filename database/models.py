import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from .database import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    fingerprint_id: Mapped[str] = mapped_column()
    weak_fingerprint_id: Mapped[str] = mapped_column()

    # for case of using multiply dna accounts. note that it
    # is just api login, not secret.
    typing_dna_api_key: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    deleted_at: Mapped[Optional[datetime]] = mapped_column()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
