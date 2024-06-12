from __future__ import annotations
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.database.repos.users import UsersRepo
from bot.settings import settings

URL = settings.db.build_postgres_url() if settings.db.used == "PostgreSQL" else settings.db.build_mysql_url()

engine = create_async_engine(URL, future=True, poolclass=NullPool)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


@dataclass
class Repositories:
    session: AsyncSession
    users: UsersRepo


@asynccontextmanager
async def get_repo() -> AsyncGenerator[Repositories, None]:
    async with sessionmaker() as s:
        yield Repositories(session=s, users=UsersRepo(s))
