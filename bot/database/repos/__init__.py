from __future__ import annotations

from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from .chat import ChatsRepo
from .users import UsersRepo


@dataclass
class Repositories:
    session: AsyncSession
    users: UsersRepo
    chats: ChatsRepo

    @staticmethod
    def get_repo(session: AsyncSession) -> Repositories:
        return Repositories(session=session, users=UsersRepo(session), chats=ChatsRepo(session))


__all__ = [
    "Repositories",
]
