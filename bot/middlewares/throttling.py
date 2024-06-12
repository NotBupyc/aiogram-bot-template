from __future__ import annotations
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from cachetools import TTLCache

from bot.settings import settings

if TYPE_CHECKING:
    from aiogram.types import TelegramObject, Update


# from app.config import settings


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.5) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id
        if user_id in settings.admins:
            return await handler(event, data)

        if user_id in self.cache:
            if event.callback_query:
                await event.callback_query.answer("Слишком часто, подожди немного", show_alert=True)
            elif event.message:
                await event.message.delete()
            return None

        self.cache[user_id] = None
        return await handler(event, data)
