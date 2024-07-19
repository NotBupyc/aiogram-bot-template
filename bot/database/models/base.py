# mypy: ignore-errors

# Imports
from __future__ import annotations

from typing import Any

from sqlalchemy import BigInteger, Column, DateTime, func
from sqlalchemy.orm import declarative_base, DeclarativeBase

Base = declarative_base()

DeclarativeBase


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, unique=True, autoincrement=True, nullable=False, primary_key=True)

    @property
    def to_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id!r})>"


class DatetimeModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), nullable=True)
