from __future__ import annotations
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Dispatcher
from cachetools import TTLCache

from bot.settings import settings

from aiogram.types import TelegramObject, CallbackQuery, Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.5) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id

        if user_id in settings.admins:
            return await handler(event, data)

        if user_id in self.cache:
            if isinstance(event, CallbackQuery):
                await event.answer("Слишком часто, подожди немного", show_alert=True)

            elif isinstance(event, Message):
                await event.delete()

            return None

        self.cache[user_id] = None
        return await handler(event, data)


def setup_throttling_middleware(dp: Dispatcher, rate_limit: float = 1.5):
    """
    Setup Throttling middleware for handlers

    :param rate_limit:
    :param dp:
    :return:
    """

    dp.message.middleware.register(ThrottlingMiddleware(rate_limit))
    dp.callback_query.middleware.register(ThrottlingMiddleware(rate_limit))
