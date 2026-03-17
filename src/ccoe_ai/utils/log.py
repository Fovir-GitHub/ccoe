import logging
from src.ccoe_ai.config import settings


def _get_log_level():
    return getattr(logging, settings.log_level, logging.INFO)


def init_logger():
    logging.basicConfig(
        level=_get_log_level(),
        format="%(asctime)s [%(levelname)s] %(message)s",
        filename="app.log",
        filemode="w",
    )
