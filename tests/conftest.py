from typing import AsyncIterator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from model_maker.database.base import session_maker


@pytest_asyncio.fixture()
async def session() -> AsyncIterator[AsyncSession]:
    async with session_maker() as sx:
        yield sx
