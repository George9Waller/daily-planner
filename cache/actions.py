import logging

from . import redis, PRINTER_ONLINE_KEY

logger = logging.getLogger(__name__)


def set_printer_is_online(printer_is_online: bool):
    cache_value = int(printer_is_online)
    redis.set(PRINTER_ONLINE_KEY, cache_value)
    logger.info(
        f"Printer '{PRINTER_ONLINE_KEY}' cached as: {cache_value}"
    )


def get_printer_is_online():
    return bool(int(redis.get(PRINTER_ONLINE_KEY)))
