from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base_models import Base
from bot.database.models.types import str_255


class Chat(Base):
    __tablename__ = "chats"
    title: Mapped[str_255] = mapped_column(nullable=False)
