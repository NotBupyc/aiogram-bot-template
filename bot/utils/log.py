from __future__ import annotations
import logging
from datetime import datetime
from logging import LogRecord, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

from bot.config import DEFAULT_TZ
from bot.settings import LogDir


class DailyRotatingFileHandler(RotatingFileHandler):
    def __init__(
        self,
        basedir: Path | str,
        mode: str = "a",
        maxBytes: int = 0,  # noqa: N803
        backupCount: int = 0,  # noqa: N803
        encoding: str | None = None,
        delay: bool = False,
    ) -> None:
        self.basedir = basedir
        self.today: datetime = datetime.now(DEFAULT_TZ)

        self.baseFilename = self.get_filename()
        RotatingFileHandler.__init__(self, self.baseFilename, mode, maxBytes, backupCount, encoding, delay)

    def get_filename(self) -> str:
        """
        @summary: Return logFile name string formatted to "today.log.alias"
        """
        self.today = datetime.now(DEFAULT_TZ)
        basename_ = self.today.strftime("%Y-%m-%d") + ".log"
        return str(Path(self.basedir) / basename_)

    def shouldRollover(self, record: LogRecord) -> int:  # noqa: N802
        """
        @summary:
        Rollover happen
        1. When the logFile size is get over maxBytes.
        2. When date is changed.

        @see: BaseRotatingHandler.emit
        """

        if self.stream is None:
            self.stream = self._open()

        if int(self.maxBytes) > 0:
            msg = f"{self.format(record)}\n"
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= int(self.maxBytes):
                return 1

        if self.today != datetime.now(DEFAULT_TZ):
            self.baseFilename = self.get_filename()
            return 1

        return 0


# Formatters
main_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s]: %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    style="%",
)

# daily handler
daily_handler = DailyRotatingFileHandler(LogDir)
daily_handler.setFormatter(main_formatter)
daily_handler.setLevel(logging.DEBUG)


# console handler
console_handler = StreamHandler()
console_handler.setFormatter(main_formatter)
console_handler.setLevel(logging.INFO)


def init_logger() -> None:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(daily_handler)

    logging.getLogger("aiogram").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    logging.getLogger("apscheduler").setLevel(logging.ERROR)
