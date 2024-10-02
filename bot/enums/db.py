from enum import StrEnum, IntEnum


class Databases(StrEnum):
    PostgreSQl = "PostgreSQL"
    MySQL = "MySQL"


class PostgreSQLDrivers(StrEnum):
    ASYNC_DRIVER = "asyncpg"


class MySQLDrivers(StrEnum):
    ASYNC_DRIVER = "asyncmy"
