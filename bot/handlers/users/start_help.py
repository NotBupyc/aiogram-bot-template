import logging

from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from bot.database.engine import Repositories
from bot.database.models import User
from bot.keyboards.inline import start_keyboard

router = Router(name=__name__)
logger = logging.getLogger()



@router.message(CommandStart(), flags={"user": False, "chat": False})
async def start(message: types.Message) -> None:
    await message.reply("Hello! I'm using a template from @Not_Bupyc!", reply_markup=start_keyboard)


@router.message(Command("help"))
async def help(message: types.Message, user: User, repo: Repositories) -> None:
    await message.reply("Hello! I'm using a template from @Not_Bupyc!", reply_markup=start_keyboard)

