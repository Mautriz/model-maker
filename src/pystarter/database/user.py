from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from .base import Base, GenericMixin


class User(GenericMixin, MappedAsDataclass, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()

    profiles: Mapped[list[Profile]] = relationship(back_populates="user", init=False)


class Profile(GenericMixin, MappedAsDataclass, Base):
    __tablename__ = "profiles"

    bio: Mapped[str] = mapped_column()

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="profiles", init=False)
