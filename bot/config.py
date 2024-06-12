import pytz
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot.settings import settings

bot = Bot(
    token=settings.bot.bot_token,
    default=DefaultBotProperties(
        parse_mode=settings.bot.parse_mode,
    ),
)

if settings.redis.use:
    redis = Redis(host=settings.redis.ip, port=settings.redis.port, password=settings.redis.password)
    storage = RedisStorage(redis=redis)
else:
    storage = MemoryStorage()

dp = Dispatcher(storage=storage)

DEFAULT_TZ = pytz.timezone("Europe/Moscow")
