from typing import AsyncIterator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from model_maker.database.base import session_maker
from model_maker.server import app


@pytest_asyncio.fixture()
async def session() -> AsyncIterator[AsyncSession]:
    async with session_maker() as sx:
        yield sx


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
