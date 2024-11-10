import logging

from aiogram import Router, F
from aiogram.filters import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
)
from aiogram.types import ChatMemberUpdated, ChatBoostUpdated
from aiogram.enums.chat_type import ChatType

from bot.database import Repositories
from bot.database.models import Chat

router = Router()
logger = logging.getLogger("chat_events")

IS_GROUP = F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP])
IS_CHANNEL = F.chat.type == ChatType.CHANNEL

@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
    IS_GROUP,
    flags={"chat": True, "chat_options": [], "user": False}
)
async def bot_added_in_chat(event: ChatMemberUpdated, repo: Repositories, chat: Chat) -> None:
    chat_ = event.chat

    await event.answer("Hello, thanks for adding me.")

    logger.info(f"Bot was added in chat {chat_.title}({chat_.id}",)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
    IS_GROUP,
    flags={"chat": True, "chat_options": [], "user": False}
)
async def bot_kicked_from_chat(event: ChatMemberUpdated, repo: Repositories, chat: Chat) -> None:
    chat_ = event.chat

    # if chat:
    #     await repo.chats.delete(chat)

    logger.info(f"Bot was kicked from chat {chat_.title}({chat_.id})")


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
    IS_GROUP,
    flags={"chat": True, "chat_options": [], "user": False}
)
async def on_user_join(event: ChatMemberUpdated, chat: Chat) -> None:
    from_user = event.from_user
    chat_ = event.chat

    await event.answer(f"👋 Hello {event.from_user.full_name}")
    logger.info(f"{from_user.full_name} was joined in {chat_.title}({chat_.id})")


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
    IS_GROUP,
    flags={"chat": True, "chat_options": [], "user": False}
)
async def on_user_leave(event: ChatMemberUpdated, chat: Chat) -> None:
    from_user = event.from_user
    chat_ = event.chat

    await event.answer(f"👋 Goodbuy {event.from_user.full_name}")
    logger.info(f"{from_user.full_name} was left from {chat_.title}({chat_.id})")


@router.chat_boost(IS_GROUP)
async def chat_boost(chat_boost: ChatBoostUpdated):
    ...

@router.removed_chat_boost(IS_GROUP)
async def remove_chat_boost(chat_boost: ChatBoostUpdated):
    ...
