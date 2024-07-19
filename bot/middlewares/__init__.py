import logging

from aiogram import Dispatcher
from bot.settings import settings
from . import database, throttling

logger = logging.getLogger("middlewares")


def setup_middlewares(dp: Dispatcher) -> None:
    database.setup(dp)
    throttling.setup(dp, rate_limit=settings.bot.rate_limit)

    logger.debug("middlewares was been load")


__all__ = ["setup_middlewares"]
