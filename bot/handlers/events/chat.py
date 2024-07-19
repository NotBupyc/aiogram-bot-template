import logging

from aiogram import Router
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
)
from aiogram.types import ChatMemberUpdated

from bot.database import Repositories
from bot.database.models import Chat

router = Router()
logger = logging.getLogger()


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION), flags={"chat": True, "chat_options": []}
)
async def bot_added_in_chat(event: ChatMemberUpdated, repo: Repositories, chat: Chat) -> None:
    await event.answer("Hello, thanks for adding me.")
    await repo.chats.create(chat_id=event.chat.id, title=event.chat.title)

    logger.info("Bot was added in chat. ID:%s, Title:%s", event.chat.id, event.chat.title)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION), flags={"chat": True, "chat_options": []}
)
async def bot_kicked_from_chat(event: ChatMemberUpdated, repo: Repositories, chat: Chat) -> None:
    await repo.chats.delete(chat)
    logger.info("Bot was kicked from chat ID:%s, Title:%s", event.chat.id, event.chat.title)


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION), flags={"chat": True, "chat_options": []})
async def on_user_join(event: ChatMemberUpdated) -> None:
    logger.info("%s was joined in %s(%s)", event.from_user.full_name, event.chat.title, event.chat.id)
    await event.answer(f"👋 Hello {event.from_user.full_name}")


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION), flags={"chat": True, "chat_options": []}
)
async def on_user_leave(event: ChatMemberUpdated) -> None:
    logger.info("%s was left from %s(%s)", event.from_user.full_name, event.chat.title, event.chat.id)

    await event.answer(f"👋 Goodbuy {event.from_user.full_name}")
