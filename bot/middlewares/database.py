from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag

from bot.database import get_repo
from bot.database.models import Chat

if TYPE_CHECKING:
    from aiogram.types import TelegramObject
    from aiogram.types import User as AiogramUser
    from aiogram.types import Chat as AiogramChat

    from bot.database.engine import Repositories

IGNORED_NAMES = ["Group", "Channel"]

logger = logging.getLogger("DatabaseMiddleware")


class GetRepo(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        us = data["event_from_user"]

        if us.first_name in IGNORED_NAMES:
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
        repo: Repositories = data["repo"]
        user_: AiogramUser = data["event_from_user"]

        if user_.first_name in IGNORED_NAMES:
            return None

        user_flag = get_flag(data, "user", default=True)

        if not user_flag:
            data["user"] = None
            return await handler(event, data)

        user_options = get_flag(data, "user_options", default=[])
        user = await repo.users.get_by_user_id(user_.id, *user_options)

        if not user:
            user = await repo.users.create_from_aiogram_model(user_)
            logger.info("New user")

        user.username = user_.username.lower() if user_.username else None

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
        repo: Repositories = data["repo"]
        chat_: AiogramChat = data["event_chat"]

        chat_flag = get_flag(data, "chat", default=False)

        if not chat_flag:
            data["chat"] = None
            return await handler(event, data)

        chat_options = get_flag(data, "chat_options", default=[])
        chat: Chat = await repo.chats.get(chat_.id, *chat_options)

        if not chat:
            chat: Chat = await repo.chats.create_from_aiogram_model(chat_)

        chat.title = chat_.title

        data["chat"] = chat
        await handler(event, data)

        await repo.chats.update(chat)
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


    # chats
    dp.my_chat_member.middleware.register(GetChat())
    dp.chat_member.middleware.register(GetChat())


