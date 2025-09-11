from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
import sys


log_format = (
    '%(asctime)s - [%(levelname)s] -  %(name)s - '
    '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(logging.Formatter(log_format))

file_handler = RotatingFileHandler(
    'time_tracker.log',
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding='UTF-8',
)
file_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def logging_decorator(func: callable) -> callable:
    """Логирует результат выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        result = func(*args, **kwargs)
        logger.info(f'Отработала функция: {func.__name__}')
        return result

    return wrapper
