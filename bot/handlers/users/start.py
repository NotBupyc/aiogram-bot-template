from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.database.engine import Repositories
from bot.database.models import User
from bot.keyboards.inline import start_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_(message: types.Message, user: User, repo: Repositories) -> None:
    await message.reply("Hello! I'm using a template from @Not_Bupyc!", reply_markup=start_keyboard)
