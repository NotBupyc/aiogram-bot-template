import logging

from aiogram import Dispatcher

from .database import GetSession, GetUser
from .throttling import ThrottlingMiddleware
from bot.settings import settings

logger = logging.getLogger("middlewares")


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.middleware.register(ThrottlingMiddleware(settings.bot.rate_limit))
    dp.update.middleware.register(GetSession())
    dp.update.middleware.register(GetUser())

    logger.debug("middlewares was been load")


__all__ = ["setup_middlewares"]
