from __future__ import annotations

from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from redis.asyncio import Redis

from bot.enums.db import Databases, PostgreSQLDrivers, MySQLDrivers

load_dotenv(find_dotenv())

ProjectDir = Path(__file__).parent.parent
BotDir = ProjectDir / "bot"
LogDir = Path(ProjectDir) / "logs"


class BotSettings(BaseSettings):
    bot_token: str
    parse_mode: Literal["MARKDOWN_V2", "MARKDOWN", "HTML"] = "HTML"
    drop_pending_updates: bool = True
    rate_limit: int | float = 1


class DatabaseSettings(BaseSettings):
    used: Databases = Databases.PostgreSQl
    ip: str
    user: str
    password: str
    name: str

    test_name: str | None = None

    model_config = SettingsConfigDict(env_prefix="DB_")

    def build_postgres_url(
            self,
            driver: PostgreSQLDrivers = PostgreSQLDrivers.ASYNC_DRIVER
    ) -> str:
        return f"postgresql+{driver}://" f"{self.user}:{self.password}" f"@{self.ip}/{self.name}"

    def build_mysql_url(
            self,
            driver: MySQLDrivers = MySQLDrivers.SYNC_DRIVER
    ) -> str:
        return f"mysql+{driver}://" f"{self.user}:{self.password}" f"@{self.ip}/{self.name}"


class RedisSettings(BaseSettings):
    use: bool
    ip: str
    port: int
    password: str

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    def get_redis(self, db: int = 0) -> Redis:
        return Redis(host=self.ip, port=self.port, password=self.password, db=db)


class Settings(BaseSettings):
    log_chat: int | None = None
    admins: list[int]
    debug_mode: bool

    bot: BotSettings = BotSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
