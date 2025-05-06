from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.database.models.custom_funcs import all_functions
from bot.database.repos import Repositories
from bot.enums.db import Databases

from bot.settings import settings

logger = logging.getLogger("Database")

URL = settings.db.build_postgres_url() if settings.db.used == Databases.PostgreSQl else settings.db.build_mysql_url()


engine = create_async_engine(URL, future=True, poolclass=NullPool, echo=settings.debug_mode)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


@asynccontextmanager
async def get_repo() -> AsyncGenerator[Repositories, None]:
    async with sessionmaker() as s:
        logger.debug("session was create")
        yield Repositories.get_repo(s)


async def create_database_custom_functions():
    async with sessionmaker() as s:
        for func in all_functions:
            await s.execute(func)
            await s.commit()

    logger.debug("all database functions was installed")
