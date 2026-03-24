import logging
import structlog
from src.ccoe_ai.config import settings


class CleanFormatter(logging.Formatter):
    """Formatter that strips ANSI escape sequences from log messages."""

    def format(self, record):
        import re

        ANSI_ESCAPE_PATTERN = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        # Format the record normally
        message = super().format(record)
        # Strip ANSI escape sequences
        return ANSI_ESCAPE_PATTERN.sub("", message)


def init_logger():
    # Determine log format from environment variable (default: console)
    log_format = settings.log_format.lower()

    # Configure structlog processors
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if log_format == "json":
        # JSON format for both console and file
        shared_processors.append(structlog.processors.JSONRenderer())
        console_formatter = logging.Formatter("%(message)s")
        file_formatter = logging.Formatter("%(message)s")
    else:
        # For console: use ConsoleRenderer with colors
        # For file: use KeyValue renderer without colors/ANSI codes
        shared_processors.append(structlog.dev.ConsoleRenderer(pad_level=False))
        console_formatter = logging.Formatter("%(message)s")
        # File gets clean key-value output without ANSI escape codes
        file_formatter = CleanFormatter("%(message)s")

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=False,
    )

    # Set up standard logging handlers with appropriate formatters
    logger = logging.getLogger()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        settings.log_file,
        mode="w",
        encoding="utf-8",
    )

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    console_handler.setLevel(log_level)
    file_handler.setLevel(log_level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
