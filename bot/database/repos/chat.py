from __future__ import annotations


from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import BaseRepo
from bot.database.models import User, Chat


class ChatsRepo(BaseRepo):
    model = Chat

    async def get_by_chat_id(self, chat_id: int, *chat_options) -> User | None:
        q = select(Chat).where(Chat.chat_id == chat_id).options(*[selectinload(i) for i in chat_options])

        return (await self.session.execute(q)).scalar()
