from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    test: int
    test1: str
