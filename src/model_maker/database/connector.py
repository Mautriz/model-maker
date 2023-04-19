from __future__ import annotations

from enum import Enum

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from .base import Base, GenericMixin


class ConnectorType(Enum):
    SQL = "sql"
    FS = "fs"


class Connector(GenericMixin, MappedAsDataclass, Base):
    __tablename__ = "users"

    type: Mapped[ConnectorType] = mapped_column()
