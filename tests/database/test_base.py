from datetime import datetime

import pytest
from sqlalchemy.orm import MappedAsDataclass

from model_maker.database.base import Base, GenericMixin


@pytest.mark.asyncio
async def test_generic_mixin() -> None:
    class GenericExtender(GenericMixin, MappedAsDataclass, Base):
        __tablename__ = "generic_extender"

        pass

    generic = GenericExtender()

    assert generic.id is not None and isinstance(generic.id, str)
    assert generic.created_at is not None and isinstance(generic.created_at, datetime)
    assert generic.updated_at is not None and isinstance(generic.updated_at, datetime)
