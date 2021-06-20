import logging
from logging.handlers import TimedRotatingFileHandler

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(module)s] [%(threadName)s] %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT
)

logger = logging.getLogger()


def get_handler(base_file_name):
    file_handler = TimedRotatingFileHandler(base_file_name, when="D", interval=1, encoding="UTF-8", backupCount=60)
    file_handler.suffix = "%Y-%m-%d"
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    return file_handler
