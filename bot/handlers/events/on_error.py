import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()
logger = logging.getLogger(__name__)


@router.errors()
async def error_handler(exception: ErrorEvent) -> None:
    update = exception.update

    update = update.message or update.callback_query
    user = update.from_user
    chat = update.chat or update.message.chat

    logger.error("Error, user=%s id=%s chat_id=%s", user.full_name, user.id, chat, exc_info=True)
