from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = Column(String(32), nullable=True)
