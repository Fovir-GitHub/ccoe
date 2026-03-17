import logging
from src.ccoe_ai.config import settings


def _get_log_level():
    return getattr(logging, settings.log_level.upper(), logging.INFO)


def _set_handler(handler: logging.Handler, log_level, formatter: logging.Formatter):
    handler.setLevel(log_level)
    handler.setFormatter(formatter)


def init_logger():
    logger = logging.getLogger()
    log_level = _get_log_level()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        settings.log_file,
        mode="w",
        encoding="utf-8",
    )
    _set_handler(console_handler, log_level, formatter)
    _set_handler(file_handler, log_level, formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
