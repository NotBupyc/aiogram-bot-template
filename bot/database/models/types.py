from typing import Annotated

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(BigInteger, unique=True, nullable=False, primary_key=True)]
integer = Annotated[int, mapped_column(Integer, server_default="0")]

str_255 = Annotated[int, mapped_column(String(200), nullable=False)]
str_128 = Annotated[int, mapped_column(String(128), nullable=False)]
str_32 = Annotated[int, mapped_column(String(32), nullable=False)]