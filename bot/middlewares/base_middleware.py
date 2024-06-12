from __future__ import annotations
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware as _BaseMiddleware

if TYPE_CHECKING:
    from aiogram.types import Update


class BaseMiddleware(_BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],  # type: ignore[override]
        event: Update,  # type: ignore[override]
        data: dict[str, Any],
    ) -> Any:
        return await handler(event, data)
