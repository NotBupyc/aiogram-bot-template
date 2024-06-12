from __future__ import annotations

from sqlalchemy import select

from .base import BaseRepo
from bot.database.models import User


class UsersRepo(BaseRepo):
    model = User

    async def get_by_user_id(self, user_id: int) -> User | None:
        q = select(User).where(User.user_id == user_id)

        return (await self.session.execute(q)).scalar()
