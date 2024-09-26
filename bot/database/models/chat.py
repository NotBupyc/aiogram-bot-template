from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
