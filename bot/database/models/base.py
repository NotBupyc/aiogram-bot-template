# mypy: ignore-errors

# Imports
from __future__ import annotations


from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.mixins import ReprMixin, SerializeMixin


class Base(DeclarativeBase, ReprMixin, SerializeMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)

