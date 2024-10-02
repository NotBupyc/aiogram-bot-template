# Aiogram3 Bot Template

---
## System dependencies
- [Python](https://www.python.org/) 3.11+
- [Poetry](https://python-poetry.org/)
- [PostgreSQL](https://www.postgresql.org/) or [MySQL](https://www.mysql.com/)
- [Redis](https://redis.io/) (Optional)

## Configure

---
### Install dependencies

#### On host
```bash
make install
````

#### For developing (include ruff, mypy, pre-commit)
```bash
make install-dev
```

---
### Configure environment variables
1. Copy file `.env.example` and rename it to .env
2. Open it and configure it
3. If you used Redis find `REDIS_USE` and set True
```
# Redis settings
REDIS_USE=True
```

---
### Installing modules for SQLAlchemy to work with databases

#### For PostgreSQL
```bash
poetry add asyncpg 
````
#### for MySQL
```bash
poetry add asyncmy
```

Default database - `PostgreSQL`. You can change this in .env `DB_USED`

### Migrations
For migrations using `Alembic`
##### Create revision
```bash
make migration message=message
```

#### upgrade database
```bash
make migrate
```
## Starting
```bash
make start
```

## Features
- Flexible choice between `PostgreSQL` and `MySQL`
- In `bot/middlewares/` there are already several middlewares in the folder(ThrottlingMiddleware)
- In `bot/filters` there are already several middlewares in the folder(IsAdmin)
- `DailyRotatingFileHandler` - logs are written to a file with the current date from 00:00 to 23:59 and stored in the `logs` folder
- `TelegramHandler` - logs are sent to the telegram chat

## Used technologies:
- [Aiogram 3.x](https://github.com/aiogram/aiogram) (Telegram bot framework)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) (working with database from Python)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (lightweight database migration tool)
- [Redis](https://redis.io/docs/) (Optional)
