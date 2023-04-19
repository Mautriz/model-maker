from datetime import datetime
from typing import AsyncIterator
from uuid import uuid4

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    MappedColumn,
    mapped_column,
)

from model_maker.config import get_config


def get_engine() -> AsyncEngine:
    return create_async_engine(get_config().database_url, poolclass=NullPool)


session_maker = async_sessionmaker(bind=get_engine())


class Base(DeclarativeBase):
    pass


class GenericMixin(MappedAsDataclass):
    id: MappedColumn[str] = mapped_column(
        primary_key=True, init=False, default_factory=lambda: uuid4().__str__()
    )

    created_at: MappedColumn[datetime] = mapped_column(
        default_factory=datetime.now,
        init=False,
    )
    updated_at: MappedColumn[datetime] = mapped_column(
        onupdate=datetime.now,
        default_factory=datetime.now,
        init=False,
    )


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
