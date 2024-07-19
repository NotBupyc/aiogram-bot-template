import contextlib
import html

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import User, Message

from bot.config import bot
from bot.database import Repositories


def get_ping_link(user: User) -> str:
    return f'<a href="tg://user?id={user.id}">{html.escape(user.full_name)}</a>'


def get_openmessage_link(user: User) -> str:
    return f'<a href="tg://openmessage?user_id={user.id}">{html.escape(user.full_name)}</a>'


async def get_user_by_username(repo: Repositories, username: str) -> User | None:
    username = username.replace("@", "").lower()

    users = await repo.users.get_users_by_username(username=username)

    if not users:
        return None

    for user in users:
        with contextlib.suppress(TelegramBadRequest):
            us = await bot.get_chat(user.user_id)
            current_username = us.username.lower() if us.username else None

            if username == current_username:
                return user

    else:
        return None


async def user_from_message(repo: Repositories, message: Message, user: User) -> User | None:
    args = message.text.split()

    if len(args) >= 2:
        arg = args[1]

        if "@" in arg:
            if arg[1:].isdigit():
                return await repo.users.get_by_user_id(int(arg[1:]))
            return await get_user_by_username(repo, arg[1:])

        if not arg.isdigit():
            return None

        return await repo.users.get(int(arg))

    if message.reply_to_message:
        reply_user = message.reply_to_message.from_user.id
        return await repo.users.get_by_user_id(reply_user)

    return None
