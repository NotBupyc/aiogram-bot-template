from sqlalchemy import BigInteger, Column, String

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(), nullable=True)
