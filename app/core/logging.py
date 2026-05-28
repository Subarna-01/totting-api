import logging
from typing import Optional
from rich.logging import RichHandler


class Logger:
    _instance: Optional["Logger"] = None
    logger: logging.Logger

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_logger("app")
        return cls._instance

    def init_logger(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            console_handler = RichHandler(
                rich_tracebacks=True,
                show_time=False,
                show_level=True,
                show_path=False,
                markup=True,
            )
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter(
                "[%(asctime)s] - %(message)s", "%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(console_format)
            self.logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger


logger = Logger().get_logger()
