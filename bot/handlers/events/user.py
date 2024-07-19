import logging

from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

router = Router()
logger = logging.getLogger()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED), F.chat.id == F.from_user.id)
async def user_blocked_bot(event: ChatMemberUpdated) -> None:
    user = event.from_user
    logger.info("%s(%s) was block bot", user.id, user.full_name)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER), F.chat.id == F.from_user.id)
async def user_unblocked_bot(event: ChatMemberUpdated) -> None:
    user = event.from_user
    logger.info("%s(%s) was unblock bot", user.id, user.full_name)

    await event.answer("Hello, thanks to unblock me.")
