from __future__ import annotations
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Dispatcher, Router

from . import admins, events, users

logger = logging.getLogger("handlers")

all_routers: list[Router] = [*users.routers, *events.routers, *admins.routers]


def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(*all_routers)

    logger.debug("%s routers has been load", len(all_routers))


__all__ = [
    "setup_routers",
]
