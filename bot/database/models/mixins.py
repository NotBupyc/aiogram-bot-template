from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, declared_attr, relationship

if TYPE_CHECKING:
    from .user_models import User

class ReprMixin:
    _repr_max_length = 25
    _repr_attrs = []

    def _repr_attrs_str(self):
        max_length = self._repr_max_length

        values = []
        for key in self._repr_attrs:
            if not hasattr(self, key):
                raise KeyError("{} has incorrect attribute '{}' in "
                               "_repr_attrs_".format(self.__class__, key))
            value = getattr(self, key)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."
            values.append("{}={}".format(key, value))

        return " ".join(values)

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__,
                                self._repr_attrs_str()
                                if self._repr_attrs_str else "")

class SerializeMixin:
    def to_dict(
            self,
            ignored_columns: list | None = None,
            relationships: bool = False
    ) -> dict:
        if ignored_columns is None:
            ignored_columns = []
        result: dict = {}

        for c in self.__table__.columns:
            if c.name in ignored_columns:
                continue
            result[c.name] = getattr(self, c.name)

        if relationships:
            for relationship_name in self.__mapper__.relationships.keys():
                try:
                    relationship_value = getattr(self, relationship_name)
                except Exception:
                    continue

                if isinstance(relationship_value, list):
                    result[relationship_name] = [
                        item.to_dict()
                        for item in relationship_value
                    ]
                else:
                    result[relationship_name] = (
                        relationship_value.to_dict()
                        if relationship_value is not None
                        else None
                    )
        return result

class DateTimeMixin:
    _datetime_func = func.now()
    _datetime_timezone: bool = False

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=cls._datetime_timezone),
            server_default=cls._datetime_func,
    )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=cls._datetime_timezone),
            server_onupdate=cls._datetime_func
        )


class UserRelationshipMixin:
    _user_id_nullable: bool = False
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_relationship_kwargs: dict = {}

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            BigInteger,
            ForeignKey("users.id"),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=cls._user_back_populates,
            **cls._user_relationship_kwargs
        )

