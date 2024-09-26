from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import mapped_column, Mapped
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = Column(String(32), nullable=True)
