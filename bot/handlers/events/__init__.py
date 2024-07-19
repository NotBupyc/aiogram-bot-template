from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import on_error, chat, user

routers: list[Router] = [on_error.router, user.router, chat.router]

_all__ = ["routers"]
