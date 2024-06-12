from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware

from bot.database import get_repo

if TYPE_CHECKING:
    from aiogram.types import TelegramObject
    from sqlalchemy import Update

    from bot.database.engine import Repositories

ignored_names = ["Group", "Channel"]

logger = logging.getLogger("DatabaseMiddleware")


class GetSession(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],  # type: ignore[override]
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in ignored_names:
            return

        async with get_repo() as repo:
            data["repo"] = repo
            logger.debug("session was create")

            await handler(event, data)


class GetUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in ignored_names:
            return None

        repo: Repositories = data["repo"]

        user = await repo.users.get_by_user_id(us.id)

        if not user:
            user = await repo.users.create(user_id=us.id, username=us.username)
            logger.info("New user")

        data["user"] = user
        return await handler(event, data)
