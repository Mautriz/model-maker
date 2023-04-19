import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model_maker.database.user import Profile, User


@pytest.mark.asyncio
async def test_user(session: AsyncSession) -> None:
    user = User(username="test", email="boh")
    session.add(user)
    session.add(Profile(bio="Hello World", user_id=user.id))
    await session.flush()

    profile = await session.scalar(
        select(Profile).join(Profile.user).where(Profile.user_id == user.id)
    )
    assert profile is not None
    assert isinstance(profile.user, User)
