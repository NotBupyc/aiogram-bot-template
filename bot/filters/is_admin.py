from __future__ import annotations


from aiogram.filters import BaseFilter

from bot.settings import settings

from aiogram.types import Message, TelegramObject, InlineQuery, CallbackQuery


class IsAdmin(BaseFilter):
    async def __call__(self, event: TelegramObject) -> bool:
        if isinstance(event, Message) and event.from_user:
            user = event.from_user.id

        elif isinstance(event, CallbackQuery) and event.message.from_user:
            user = event.message.from_user.id

        elif isinstance(event, InlineQuery) and event.from_user:
            user = event.from_user.id
        else:
            user = None

        if not user:
            return False

        if user in settings.admins:
            return True

        return False
