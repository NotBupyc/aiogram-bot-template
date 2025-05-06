from __future__ import annotations

import asyncio
import html
import logging
import traceback
from datetime import datetime
from logging import LogRecord, StreamHandler
from logging.handlers import RotatingFileHandler

from aiogram import Bot

from bot.config import DEFAULT_TZ, bot
from bot.settings import settings, LogDir

TIME_FORMAT = "%Y-%m-%d"

MAIN_FORMATTER = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s]: %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    style="%",
)


class DailyRotatingFileHandler(RotatingFileHandler):
    def __init__(
        self,
        mode: str = "a",
        maxBytes: int = 0,  # noqa: N803
        backupCount: int = 0,  # noqa: N803
        encoding: str | None = None,
        delay: bool = False,
    ) -> None:
        self.baseFilename = self.get_filename()
        self.today = self._today()
        RotatingFileHandler.__init__(self, self.baseFilename, mode, maxBytes, backupCount, encoding, delay)

    def _today(self) -> datetime:
        self.today = datetime.now()
        return self.today

    @staticmethod
    def get_filename() -> str:
        """
        @summary: Return logFile name string formatted to "today.log.alias"
        """
        today = datetime.now(DEFAULT_TZ)
        file_name = today.strftime(TIME_FORMAT) + ".log"
        return str(LogDir / file_name)

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

        if self.today != self._today:
            self.baseFilename = self.get_filename()
            return 1

        self.baseFilename = self.get_filename()
        return 0


class TelegramHandler(logging.Handler):
    ERROR_MESSAGE = (
        "<b> 🎯 Source: {module}:{line} in {func} </b> \n"
        "<b> ❓ Error: {error} </b>\n"
        '<pre><code class="language-py">{traceback}</code></pre> \n'
    )
    ERROR_MESSAGE_WITHOUT_EXC_INFO = "ERROR: {message}"
    WARNING_MESSAGE = ""
    INFO_MESSAGE = "{date}: {message}"

    def __init__(self, bot: Bot, log_chat_id: int, max_message_lenght: int = 4096, timeout: float = 60):
        super().__init__()

        self.bot = bot
        self.log_chat_id = log_chat_id
        self.max_message_lenght = max_message_lenght
        self.timeout = timeout
        self.buffer: list[str] = []

        self.install()

    def install(self):
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.queue_poller())

    async def queue_poller(self) -> None:
        while True:
            await asyncio.sleep(self.timeout)
            if self.buffer:
                await self.send_logs()

    def emit(self, record: LogRecord):
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            self.send_extra_logs(record)
            return

        if record.levelno == logging.DEBUG:
            return

        self.add_log(record)

    async def send(self, message: str):
        await self.bot.send_message(self.log_chat_id, message)

    def send_extra_logs(self, record: LogRecord) -> None:
        exc = "\n".join(traceback.format_exc().splitlines()[-13:])
        if not record.exc_info:
            message = self.ERROR_MESSAGE_WITHOUT_EXC_INFO.format(message=record.message)
        else:
            error = f"{record.exc_info[0].__name__}: {str(record.exc_info[1])}"

            message = self.ERROR_MESSAGE.format(
                module=html.escape(f"<file {record.filename}>"),
                line=record.lineno,
                func=html.escape(record.funcName),
                error=html.escape(error),
                traceback=html.escape(exc),
            )
        self.loop.create_task(self.send(message))

    async def send_logs(self) -> None:
        logs = self.split_logs()

        for i in logs:
            if not i:
                return
            await self.send("\n".join(i))

        self.clear_logs()

    def clear_logs(self) -> None:
        self.buffer = []

    def add_log(self, record: LogRecord) -> None:
        text = self.INFO_MESSAGE.format(date=datetime.now().strftime("%H:%M:%S"), message=record.getMessage())
        self.buffer.append(text)

    def split_logs(self) -> list[list[str]]:
        tmp_list = [[]]
        tmp_length = 0

        for i in self.buffer:
            if tmp_length + len(i) > self.max_message_lenght:
                tmp_list.append([])
                tmp_length = 0

            tmp_list[-1].append(i)
            tmp_length += len(i)

        return tmp_list


def _get_daily_handler() -> DailyRotatingFileHandler:
    daily_handler = DailyRotatingFileHandler()
    daily_handler.setFormatter(MAIN_FORMATTER)
    daily_handler.setLevel(logging.DEBUG)

    return daily_handler


def _get_telegram_handler() -> TelegramHandler:
    telegram_handler = TelegramHandler(bot=bot, log_chat_id=settings.log_chat)
    telegram_handler.setFormatter(MAIN_FORMATTER)
    telegram_handler.setLevel(logging.INFO)

    return telegram_handler


def _get_console_handler() -> StreamHandler:
    console_level = logging.DEBUG if settings.debug_mode else logging.INFO

    console_handler = StreamHandler()
    console_handler.setFormatter(MAIN_FORMATTER)
    console_handler.setLevel(console_level)
    return console_handler


def init_logger() -> None:
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(_get_daily_handler())
    logging.getLogger().addHandler(_get_console_handler())

    logging.getLogger("aiogram").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    logging.getLogger("apscheduler").setLevel(logging.ERROR)
    logging.getLogger("tzlocal").setLevel(logging.ERROR)
