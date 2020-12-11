import logging
from app.main.log import logger, get_handler

logger.addHandler(get_handler("log/test_server.log"))

logger.setLevel(logging.INFO)
