import asyncio
import logging
from datetime import datetime

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot.config import DEFAULT_TZ, bot, dp
from bot.settings import settings
from bot.utils.log import init_logger

init_logger()
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Start"),
        BotCommand(command="help", description="Help"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup(bot: Bot) -> None:
    await set_commands(bot)

    user = await bot.me()

    logger.info("Bot was started %s(%s)", user.full_name, user.id)
    logger.info("Use redis? %s", settings.redis.use)

    if not settings.log_chat:
        return

    await bot.send_message(
        settings.log_chat,
        f"*Starting!* _(⏰{datetime.now(DEFAULT_TZ).strftime('%d.%m.%Y %H:%M:%S')})_",
        parse_mode="Markdown",
    )


async def on_shutdown(bot: Bot) -> None:
    logger.info("Bot stopped")

    if not settings.log_chat:
        return

    await bot.send_message(
        settings.log_chat, f"*Exit* _(⏰{datetime.now(DEFAULT_TZ).strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown"
    )


async def _main() -> None:
    logger.info("Starting bot...")

    from bot.handlers import setup_routers
    from bot.middlewares import setup_middlewares

    setup_middlewares(dp)
    setup_routers(dp)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=settings.bot.drop_pending_updates)

    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
