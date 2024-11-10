from __future__ import annotations

from aiogram.types import Chat as AiogramChat

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import BaseRepo
from bot.database.models import User, Chat


class ChatsRepo(BaseRepo):
    model = Chat

    async def create_from_aiogram_model(self, chat: AiogramChat) -> Chat:
        us = await self.create(
            id=chat.id,
            title=chat.title
        )
        return us

