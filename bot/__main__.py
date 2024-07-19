import asyncio
import contextlib
import logging
from datetime import datetime

from aiogram import Bot

from bot.config import DEFAULT_TZ, bot, dp
from bot.settings import settings
from bot.utils.bot_commands import set_commands
from bot.utils.connect_to_services import test_redis_pool, test_database_pool
from bot.utils.log import init_logger, _get_telegram_handler
from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares

init_logger()
logger = logging.getLogger(__name__)


@dp.startup()
async def on_startup(bot: Bot) -> None:
    await set_commands(bot)
    user = await bot.me()

    logger.info("Bot was started %s(%s)", user.full_name, user.id)

    if not settings.log_chat:
        return

    await bot.send_message(
        settings.log_chat,
        f"*Starting!* _(⏰{datetime.now(DEFAULT_TZ).strftime('%d.%m.%Y %H:%M:%S')})_",
        parse_mode="Markdown",
    )


@dp.shutdown()
async def on_shutdown(bot: Bot) -> None:
    logger.info("Bot stopped")

    if not settings.log_chat:
        return

    await bot.send_message(
        settings.log_chat, f"*Exit* _(⏰{datetime.now(DEFAULT_TZ).strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown"
    )


async def _main() -> None:
    logger.info("Starting bot...")

    if settings.redis.use:
        try:
            await test_redis_pool()
        except ConnectionError as e:
            logger.error(
                "Failed connection to Redis",
                e,
            )
            exit(1)
    try:
        await test_database_pool()
    except ConnectionRefusedError as e:
        logger.error(
            "Failed connection to %s: %s",
            settings.db.used,
            e,
        )
        exit(1)

    setup_middlewares(dp)
    setup_routers(dp)

    await bot.delete_webhook(drop_pending_updates=settings.bot.drop_pending_updates)

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        logging.getLogger().addHandler(_get_telegram_handler())
        await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
