from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(text="Bupyc", url="https://t.me/Not_Bupyc"),
            InlineKeyboardButton(text="Template", url="https://github.com/NotBupyc/aiogram-bot-template"),
        ]
    ]
).as_markup()
