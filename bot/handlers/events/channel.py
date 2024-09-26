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

IS_CHANNEL = F.chat.type == ChatType.CHANNEL


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION),
    IS_CHANNEL,
    flags={"chat": False, "user": False}
)
async def bot_added_in_channel(event: ChatMemberUpdated) -> None:
    channel = event.chat

    logger.info(f"Bot was added in channel {channel.title}({channel.id})")


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION),
    IS_CHANNEL,
    flags={"chat": False, "user": False}
)
async def bot_kicked_from_chat(event: ChatMemberUpdated) -> None:
    channel = event.chat

    logger.info(f"Bot was kicked from channel {channel.title}({channel.id})")


@router.chat_boost(
    IS_CHANNEL,
    flags={"chat": False, "user": False}
)
async def channel_boost(chat_boost: ChatBoostUpdated):
    ...

@router.removed_chat_boost(
    IS_CHANNEL,
    flags={"chat": False, "user": False}
)
async def remove_channel_boost(chat_boost: ChatBoostUpdated):
    ...