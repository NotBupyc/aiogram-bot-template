from aiogram.filters import BaseFilter as _BaseFilter
from aiogram.types import Message


class ExampleFilter(_BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:  # noqa: ARG002
        return True
