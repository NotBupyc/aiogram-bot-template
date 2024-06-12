from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Router

from . import start

routers: list[Router] = [start.router]

_all__ = ["routers"]
