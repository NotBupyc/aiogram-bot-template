from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag

from bot.database import get_repo

if TYPE_CHECKING:
    from aiogram.types import TelegramObject

    from bot.database.engine import Repositories

_IGNORED_NAMES = ["Group", "Channel"]

logger = logging.getLogger("DatabaseMiddleware")


class GetRepo(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in _IGNORED_NAMES:
            return

        async with get_repo() as repo:
            data["repo"] = repo

            await handler(event, data)


class GetUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in _IGNORED_NAMES:
            return None

        repo: Repositories = data["repo"]

        user_flag = get_flag(data, "user", default=True)

        if not user_flag:
            data["user"] = None
            return await handler(event, data)

        user_options = get_flag(data, "user_options", default=[])
        user = await repo.users.get_by_user_id(us.id, *user_options)

        if not user:
            user = await repo.users.create(user_id=us.id, username=us.username)
            logger.info("New user")

        user.username = us.username.lower() if us.username else None

        data["user"] = user

        await handler(event, data)

        await repo.users.update(user)
        return None


class GetChat(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        chat = data["event_chat"]
        repo: Repositories = data["repo"]

        chat_flag = get_flag(data, "chat", default=False)

        if not chat_flag:
            data["chat"] = None
            return await handler(event, data)
        #
        chat_options = get_flag(data, "chat_options", default=[])

        chat = await repo.chats.get_by_chat_id(chat.id, *chat_options)
        data["chat"] = chat

        await handler(event, data)
        return None


def setup_get_repo_middleware(dp: Dispatcher):
    """
    Setup GetRepo middleware for handlers
    :param dp:
    :return:
    """

    # default updates
    dp.message.middleware.register(GetRepo())
    dp.callback_query.middleware.register(GetRepo())
    dp.inline_query.middleware.register(GetRepo())

    # chats
    dp.my_chat_member.middleware.register(GetRepo())
    dp.chat_member.middleware.register(GetRepo())


def setup_get_user_middleware(dp: Dispatcher):
    """
    Setup GetUser middleware for handlers

    :param dp:
    :return:
    """

    dp.message.middleware.register(GetUser())
    dp.callback_query.middleware.register(GetUser())
    dp.inline_query.middleware.register(GetUser())

    # chats
    dp.my_chat_member.middleware.register(GetUser())
    dp.chat_member.middleware.register(GetUser())


def setup_get_chat_middleware(dp: Dispatcher):
    """
    Setup GetChat middleware for handlers

    :param dp:
    :return:
    """

    dp.message.middleware.register(GetChat())
    dp.callback_query.middleware.register(GetChat())
    dp.inline_query.middleware.register(GetChat())

    # chats
    dp.my_chat_member.middleware.register(GetChat())
    dp.chat_member.middleware.register(GetChat())


