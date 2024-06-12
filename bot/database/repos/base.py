from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Any, Sequence, TypeVar

from sqlalchemy import func, select

from bot.database.models.base import BaseModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


Model = TypeVar("Model", bound=BaseModel)


class BaseRepo(ABC):
    model: Model

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        if self.model is None:
            msg = "It is necessary to define the 'model' attribute in the descendant class."
            raise NotImplementedError(msg)

    async def create(self, **kwargs: dict[str, Any]) -> Model:
        db_obj = self.model(**kwargs)
        self.session.add(db_obj)
        await self.session.commit()

        await self.session.refresh(db_obj)
        return db_obj

    async def get(self, db_object_id: int) -> Model | None:
        q = select(self.model).where(self.model.id == db_object_id)

        return (await self.session.execute(q)).scalar()

    async def delete(self, db_object: Model) -> None:
        await self.session.delete(db_object)
        await self.session.commit()

    async def update(self, db_object: Model) -> Model:
        self.session.add(db_object)
        await self.session.commit()

        await self.session.refresh(db_object)
        return db_object

    async def get_all(self, count: bool = False) -> Sequence[Model] | int:
        if count:
            result = await self.session.execute(select(func.count()).select_from(self.model))
            return result.scalar_one()

        result = await self.session.execute(select(self.model))
        return result.scalars().all()
