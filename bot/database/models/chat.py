from sqlalchemy import Column, String, BigInteger

from bot.database.models.base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    chat_id = Column(BigInteger, unique=True, nullable=False)
    title = Column(String, nullable=False)
