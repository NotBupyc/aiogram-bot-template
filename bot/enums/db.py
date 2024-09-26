from enum import StrEnum, IntEnum


class Databases(StrEnum):
    PostgreSQl = "PostgreSQL"
    MySQL = "MySQL"


class PostgreSQLDrivers(StrEnum):
    SYNC_DRIVER = "psycopg2"
    ASYNC_DRIVER = "asyncpg"


class MySQLDrivers(StrEnum):
    SYNC_DRIVER = "pymysql"
    ASYNC_DRIVER = "asyncmy"
