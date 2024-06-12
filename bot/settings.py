from __future__ import annotations
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())

BotDir = Path(__file__).parent
ProjectDir = BotDir.parent
LogDir = Path(ProjectDir) / "logs"


class BotSettings(BaseSettings):
    bot_token: str
    parse_mode: Literal["MARKDOWN_V2", "MARKDOWN", "HTML"] = "HTML"
    drop_pending_updates: bool = True
    rate_limit: int | float = 1


class DatabaseSettings(BaseSettings):
    used: Literal["PostgreSQL", "MySQL"] = "PostgreSQL"
    ip: str
    user: str
    password: str
    name: str

    model_config = SettingsConfigDict(env_prefix="DB_")

    def build_postgres_url(self, driver: Literal["psycopg2", "asyncpg"] = "asyncpg") -> str:
        return f"postgresql+{driver}://" f"{self.user}:{self.password}" f"@{self.ip}/{self.name}"

    def build_mysql_url(self, driver: Literal["pymysql", "asyncmy"] = "asyncmy") -> str:
        return f"mysql+{driver}://" f"{self.user}:{self.password}" f"@{self.ip}/{self.name}"


class RedisSettings(BaseSettings):
    use: bool
    ip: str | None = None
    port: str | None = None
    password: str | None = None

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def build_redis_url(self) -> str:
        if self.password:
            return f"redis://{self.password}@{self.ip}:{self.port}/0"
        return f"redis://{self.ip}:{self.port}/0"


class Settings(BaseSettings):
    log_chat: int | None = None
    admins: list[int]

    bot: BotSettings = BotSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
