# mypy: ignore-errors

# Imports
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, Column, DateTime, func, Integer
from sqlalchemy.orm import declarative_base, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)

    @property
    def to_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id!r})>"


class DatetimeModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), server_onupdate=func.now(), nullable=True)
