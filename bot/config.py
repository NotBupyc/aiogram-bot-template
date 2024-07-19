import pytz
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from .settings import settings

bot = Bot(
    token=settings.bot.bot_token,
    default=DefaultBotProperties(
        parse_mode=settings.bot.parse_mode,
    ),
)

storage: BaseStorage
if settings.redis.use:
    storage = RedisStorage(settings.redis.get_redis())
else:
    storage = MemoryStorage()

dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.USER_IN_CHAT)

DEFAULT_TZ = pytz.timezone("Europe/Moscow")
