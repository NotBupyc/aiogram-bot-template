from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import BaseRepo
from bot.database.models import User


class UsersRepo(BaseRepo):
    model = User

    async def get_by_user_id(self, user_id: int, *user_options) -> User | None:
        q = select(User).where(User.id == user_id).options(*[selectinload(i) for i in user_options])

        return (await self.session.execute(q)).scalar()

    async def get_users_by_username(self, username: str) -> Sequence[User]:
        q = select(User).where(User.username == username)

        return (await self.session.execute(q)).scalars().all()
