import logging
from typing import cast

from aiogram import Router
from aiogram.types import ErrorEvent, Update, Message

router = Router()
logger = logging.getLogger(__name__)


@router.errors()
async def error_handler(exception: ErrorEvent) -> None:
    update: Update = exception.update

    if message := update.message:
        user = message.from_user
        chat = message.chat

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = chat.id

    elif query := update.callback_query:
        message = cast(Message, query.message)

        user = message.from_user if message.from_user else None
        chat = message.chat

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = chat.id

    elif inline := update.inline_query:
        user = inline.from_user

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = None

    elif my_chat := update.my_chat_member:
        user = my_chat.from_user

        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = None

    elif chat_member := update.chat_member:
        user = chat_member.from_user
        chat = chat_member.chat
        user_id = user.id if user else None
        user_full_name = user.full_name if user else None

        chat_id = chat.id
    else:
        logger.warning("Unknow update, %s", exception.update)
        return

    logger.error(
        f"User={user_full_name} id={user_id} chat_id={chat_id if chat_id else 'No chat'}", exc_info=True
    )
