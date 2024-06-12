import logging

from aiogram import Router, types
from aiogram.filters import Command

from bot.filters import IsAdmin
from bot.messages import BOT_INFO
from bot.utils.misc import bot_info_dict

router = Router()
logger = logging.getLogger(__name__)

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("botinfo"))
async def bot_info(message: types.Message) -> None:
    text = BOT_INFO.format(**await bot_info_dict())
    await message.answer(text=text)
