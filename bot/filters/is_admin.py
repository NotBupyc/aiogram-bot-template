from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram.filters import BaseFilter

from bot.settings import settings

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message


class IsAdmin(BaseFilter):
    async def __call__(self, update: CallbackQuery | Message) -> bool:
        if update.from_user.id in settings.admins:
            return True

        return False
